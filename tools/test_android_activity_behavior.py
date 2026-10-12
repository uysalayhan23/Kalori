#!/usr/bin/env python3
"""Execute MainActivity result-handler behavior against disposable Android test stubs."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("stubcheck", ROOT/"tools/check_android_java_stubs.py")
stubcheck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stubcheck)

HARNESS = r'''
package com.kalori.journal;
import android.content.ContentResolver;
import android.content.Intent;
import android.net.Uri;
import android.webkit.ValueCallback;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.lang.reflect.Field;

public final class ActivityBehaviorHarness {
 static class CheckActivity extends MainActivity {
   int opened=0,closed=0;
   boolean failWrite=false,failClose=false;
   ByteArrayOutputStream contents=new ByteArrayOutputStream();
   public void handle(int request,int result,Intent intent){onActivityResult(request,result,intent);}
   @Override public ContentResolver getContentResolver(){
      return new ContentResolver(){
         @Override public OutputStream openOutputStream(Uri uri,String mode){
            opened++;
            return new OutputStream(){
               public void write(int b)throws IOException {
                  if(failWrite)throw new IOException("failed write");
                  contents.write(b);
               }
               public void close()throws IOException {
                  closed++;
                  if(failClose)throw new IOException("failed close");
               }
            };
         }
      };
   }
 }
 static void set(MainActivity activity,String name,Object value)throws Exception{
   Field field=MainActivity.class.getDeclaredField(name);field.setAccessible(true);field.set(activity,value);
 }
 static Object get(MainActivity activity,String name)throws Exception{
   Field field=MainActivity.class.getDeclaredField(name);field.setAccessible(true);return field.get(activity);
 }
 static void check(boolean condition,String message){if(!condition)throw new AssertionError(message);}
 static Intent document(){
    return new Intent("document"){@Override public Uri getData(){return new Uri();}};
 }
 public static void main(String[] args)throws Exception{
   CheckActivity a=new CheckActivity();
   final int[] responses={0};
   ValueCallback<Uri[]> callback=value->{responses[0]++;check(value==null,"cancel should return null");};
   set(a,"uploadCallback",callback);
   a.handle(301,0,null);
   check(responses[0]==1,"picker callback not called on cancellation");
   check(get(a,"uploadCallback")==null,"picker callback not released");

   set(a,"pendingBackup","{\"entries\":[],\"water\":{}}");
   a.handle(302,0,null);
   check(get(a,"pendingBackup")==null,"cancel must release backup");
   check(a.opened==0,"cancel must not open output");

   set(a,"pendingBackup","{\"entries\":[],\"water\":{}}");
   a.handle(302,-1,document());
   check(a.opened==1 && a.closed==1,"successful backup must close stream");
   check(a.contents.size()>0,"backup must write bytes");
   check(get(a,"pendingBackup")==null,"backup must release payload");

   a.failWrite=true;
   set(a,"pendingBackup","{\"entries\":[],\"water\":{}}");
   a.handle(302,-1,document());
   check(a.opened==2 && a.closed==2,"failed write must close stream");
   check(get(a,"pendingBackup")==null,"write failure must release payload");

   a.failWrite=false;a.failClose=true;
   set(a,"pendingBackup","{\"entries\":[],\"water\":{}}");
   a.handle(302,-1,document());
   check(a.opened==3 && a.closed==3,"close failure must be attempted");
   check(get(a,"pendingBackup")==null,"close failure must release payload");

   CheckActivity recreated=new CheckActivity();
   recreated.handle(302,-1,document());
   check(recreated.opened==0,"recreated Activity must not write missing backup");
   System.out.println("PASS: picker cancel, backup cancel, successful write, write/close errors and recreation.");
 }
}
'''

def main():
    if not stubcheck.SOURCE.is_file(): raise SystemExit("Missing MainActivity.java")
    javac=stubcheck.shutil.which("javac")
    java=stubcheck.shutil.which("java")
    if not javac or not java: raise SystemExit("NOT RUN: Java toolchain missing")
    with tempfile.TemporaryDirectory(prefix="kalori-activity-behavior-") as tmp:
        root=Path(tmp)
        files=[]
        for name,body in stubcheck.STUBS.items():
            dest=root/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(body,encoding="utf-8")
            files.append(str(dest))
        harness=root/"com/kalori/journal/ActivityBehaviorHarness.java"
        harness.parent.mkdir(parents=True,exist_ok=True)
        harness.write_text(HARNESS,encoding="utf-8")
        command=[javac,"--release","17","-encoding","UTF-8","-d",str(root/"classes"),
                 *files,str(stubcheck.SOURCE),str(harness)]
        build=subprocess.run(command,capture_output=True,text=True)
        if build.returncode:
            print(build.stderr,file=sys.stderr)
            raise SystemExit(build.returncode)
        result=subprocess.run([java,"-cp",str(root/"classes"),
                "com.kalori.journal.ActivityBehaviorHarness"],capture_output=True,text=True)
        if result.stdout:print(result.stdout.strip())
        if result.returncode:
            print(result.stderr,file=sys.stderr)
            raise SystemExit(result.returncode)

if __name__=="__main__": main()
