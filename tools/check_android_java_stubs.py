#!/usr/bin/env python3
"""Compile MainActivity with temporary API surface stubs. Never build an APK."""
from pathlib import Path
import shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"android/app/src/main/java/com/kalori/journal/MainActivity.java"
STUBS={
"android/app/Activity.java":"""package android.app;
import android.os.Bundle;import android.content.Intent;import android.content.ContentResolver;
public class Activity {
 public static final int RESULT_OK=-1;
 protected void onCreate(Bundle b){} protected void onSaveInstanceState(Bundle b){} protected void onPause(){} protected void onResume(){} protected void onActivityResult(int req,int result,Intent data){} protected void onDestroy(){}
 public void onBackPressed(){} public void setContentView(Object v){} public void runOnUiThread(Runnable r){} public void startActivity(Intent i){} public void startActivityForResult(Intent i,int r){}
 public ContentResolver getContentResolver(){return null;}
}""",
"android/os/Bundle.java":"""package android.os; public class Bundle {public Bundle getBundle(String key){return null;} public void putBundle(String key,Bundle val){}}""",
"android/content/Intent.java":"""package android.content;import android.net.Uri;
public class Intent {
 public static final String ACTION_VIEW="view",ACTION_OPEN_DOCUMENT="open",ACTION_CREATE_DOCUMENT="create",CATEGORY_OPENABLE="openable",EXTRA_TITLE="title";
 public Intent(String action){} public Intent(String action,Uri uri){}
 public Intent addCategory(String category){return this;} public Intent setType(String type){return this;} public Intent putExtra(String key,String value){return this;}
 public Uri getData(){return null;}
}""",
"android/content/ActivityNotFoundException.java":"""package android.content;public class ActivityNotFoundException extends RuntimeException {}""",
"android/content/ContentResolver.java":"""package android.content;import android.net.Uri;import java.io.OutputStream;import java.io.FileNotFoundException;
public class ContentResolver {public OutputStream openOutputStream(Uri uri,String mode)throws FileNotFoundException{return null;}}""",
"android/net/Uri.java":"""package android.net;public class Uri {public String getScheme(){return null;}public String toString(){return "";}}""",
"android/util/Log.java":"""package android.util;public class Log {public static int e(String t,String m,Throwable x){return 0;}public static int w(String t,String m){return 0;}}""",
"android/widget/Toast.java":"""package android.widget;import android.app.Activity;
public class Toast {public static final int LENGTH_LONG=1,LENGTH_SHORT=0;public static final java.util.List<String> messages=new java.util.ArrayList<>();private String message;public static Toast makeText(Activity a,String s,int len){Toast t=new Toast();t.message=s;return t;}public void show(){messages.add(message);}}""",
"android/webkit/JavascriptInterface.java":"""package android.webkit;@java.lang.annotation.Retention(java.lang.annotation.RetentionPolicy.RUNTIME)public @interface JavascriptInterface {}""",
"android/webkit/ValueCallback.java":"""package android.webkit;public interface ValueCallback<T>{void onReceiveValue(T value);}""",
"android/webkit/WebSettings.java":"""package android.webkit;public class WebSettings {
 public static final int MIXED_CONTENT_NEVER_ALLOW=1;
 public void setJavaScriptEnabled(boolean b){}public void setDomStorageEnabled(boolean b){}public void setAllowFileAccess(boolean b){}public void setAllowContentAccess(boolean b){}
 public void setAllowFileAccessFromFileURLs(boolean b){}public void setAllowUniversalAccessFromFileURLs(boolean b){}public void setMixedContentMode(int m){}public void setJavaScriptCanOpenWindowsAutomatically(boolean b){}
}""",
"android/webkit/WebChromeClient.java":"""package android.webkit;import android.net.Uri;
public class WebChromeClient {public static class FileChooserParams{} public boolean onShowFileChooser(WebView v,ValueCallback<Uri[]> callback,FileChooserParams params){return false;}}""",
"android/webkit/WebResourceRequest.java":"""package android.webkit;import android.net.Uri;
public interface WebResourceRequest {Uri getUrl();boolean isForMainFrame();}""",
"android/webkit/WebViewClient.java":"""package android.webkit;public class WebViewClient {
 public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest request){return false;}}""",
"android/webkit/WebView.java":"""package android.webkit;import android.app.Activity;import android.os.Bundle;
public class WebView {public WebView(Activity a){}public WebSettings getSettings(){return new WebSettings();}
 public void addJavascriptInterface(Object obj,String name){}public void removeJavascriptInterface(String name){}
 public void setWebChromeClient(WebChromeClient c){}public void setWebViewClient(WebViewClient c){}
 public void loadUrl(String u){}public Object restoreState(Bundle b){return null;}public Object saveState(Bundle b){return null;}
 public void onPause(){}public void onResume(){}public boolean canGoBack(){return false;}public void goBack(){}
 public void stopLoading(){}public void destroy(){}
}""",
"org/json/JSONArray.java":"""package org.json;public class JSONArray {}""",
"org/json/JSONObject.java":"""package org.json;public class JSONObject {public JSONObject(String s){}public Object opt(String key){return null;}}"""
}
def main():
    if not SOURCE.is_file():raise SystemExit("Missing MainActivity.java")
    javac=shutil.which("javac")
    if not javac:raise SystemExit("NOT RUN: javac unavailable; SDK-free Java check required")
    with tempfile.TemporaryDirectory(prefix="kalori-javac-") as tmp:
        base=Path(tmp);java_files=[]
        for rel,body in STUBS.items():
            dest=base/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(body,encoding="utf-8");java_files.append(str(dest))
        result=subprocess.run([javac,"--release","17","-encoding","UTF-8","-d",str(base/"classes"),*java_files,str(SOURCE)],capture_output=True,text=True)
        if result.returncode:
            print(result.stderr,file=sys.stderr)
            raise SystemExit(result.returncode)
        expected=base/"classes/com/kalori/journal/MainActivity.class"
        if not expected.is_file():raise SystemExit("FAIL: javac returned success but MainActivity.class was not generated")
        print("PASS: MainActivity.java javac --release 17 with temporary Android API stubs; no SDK, Gradle or APK.")
if __name__=="__main__":main()
