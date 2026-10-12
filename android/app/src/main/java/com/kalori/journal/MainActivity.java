package com.kalori.journal;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebChromeClient;
import android.webkit.ValueCallback;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.webkit.WebResourceRequest;
import android.content.Intent;
import android.net.Uri;
import android.webkit.JavascriptInterface;
import java.io.OutputStream;
import java.io.IOException;
import android.widget.Toast;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;
import org.json.JSONArray;

public class MainActivity extends Activity {
    private WebView view;
    private static final int FILE_PICKER_REQUEST=301;
    private static final int BACKUP_SAVE_REQUEST=302;
    private String pendingBackup;
    private ValueCallback<Uri[]> uploadCallback;
    private static final String ASSET_ORIGIN = "file:///android_asset/";
    private static final String WEBVIEW_STATE = "kalori_webview_state";
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        view = new WebView(this);
        view.getSettings().setJavaScriptEnabled(true);
        view.getSettings().setDomStorageEnabled(true);
        view.getSettings().setAllowFileAccess(true);
        view.getSettings().setAllowContentAccess(true);
        view.getSettings().setAllowFileAccessFromFileURLs(false);
        view.getSettings().setAllowUniversalAccessFromFileURLs(false);
        view.getSettings().setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        view.getSettings().setJavaScriptCanOpenWindowsAutomatically(false);
        view.addJavascriptInterface(new Object() {
            @JavascriptInterface public void saveBackup(String json) {
                if(json==null || json.length()>5_000_000)return;
                try {
                    JSONObject value=new JSONObject(json);
                    if(!(value.opt("entries") instanceof JSONArray) || !(value.opt("water") instanceof JSONObject))return;
                } catch(Exception error){return;}
                runOnUiThread(()->{
                    if(pendingBackup!=null)return;
                    pendingBackup=json;
                    Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("application/json");
                    intent.putExtra(Intent.EXTRA_TITLE,"kalori-kayitlarim.json");
                    try {startActivityForResult(intent,BACKUP_SAVE_REQUEST);}
                    catch(android.content.ActivityNotFoundException error){pendingBackup=null;Toast.makeText(MainActivity.this,"Dosya kaydetme ekranı açılamadı.",Toast.LENGTH_LONG).show();}
                });
            }
        },"KaloriAndroid");
        view.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if(uploadCallback!=null){uploadCallback.onReceiveValue(null);uploadCallback=null;}
                uploadCallback=callback;
                Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("application/json");
                try { startActivityForResult(intent,FILE_PICKER_REQUEST);return true; }
                catch(android.content.ActivityNotFoundException error){uploadCallback=null;callback.onReceiveValue(null);return false;}
            }
        });
        view.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest request) {
                Uri uri=request.getUrl();
                if ("file".equals(uri.getScheme()) && uri.toString().startsWith(ASSET_ORIGIN)) return false;
                if (request.isForMainFrame() && "https".equals(uri.getScheme())) {
                    try {startActivity(new Intent(Intent.ACTION_VIEW,uri));}
                    catch(android.content.ActivityNotFoundException error){android.util.Log.w("Kalori","No HTTPS handler");}
                }
                return true;
            }
        });
        setContentView(view);
        Bundle previous=savedInstanceState==null?null:savedInstanceState.getBundle(WEBVIEW_STATE);
        if(previous==null || view.restoreState(previous)==null){view.loadUrl(ASSET_ORIGIN+"index.html");}
    }
    @Override protected void onSaveInstanceState(Bundle outState) {
        if(view!=null){
            Bundle webState=new Bundle();
            view.saveState(webState);
            outState.putBundle(WEBVIEW_STATE,webState);
        }
        super.onSaveInstanceState(outState);
    }
    @Override protected void onPause() {
        if(view!=null)view.onPause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if(view!=null)view.onResume();
    }
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data) {
        super.onActivityResult(requestCode,resultCode,data);
        if(requestCode==BACKUP_SAVE_REQUEST){
            String json=pendingBackup;pendingBackup=null;
            if(resultCode==RESULT_OK && data!=null && data.getData()!=null && json==null){
                Toast.makeText(this,"Uygulama yeniden açıldığı için yedekleme tamamlanamadı. Lütfen yeniden deneyin.",Toast.LENGTH_LONG).show();
            }
            if(resultCode==RESULT_OK && data!=null && data.getData()!=null && json!=null){
                boolean saved=false;
                try(OutputStream stream=getContentResolver().openOutputStream(data.getData(),"w")){
                    if(stream==null)throw new IOException("No output stream");
                    stream.write(json.getBytes(StandardCharsets.UTF_8));
                    saved=true;
                }catch(Exception error){android.util.Log.e("Kalori","Backup export failed",error);Toast.makeText(this,"Yedek kaydedilemedi. Farklı bir dosya konumu deneyin.",Toast.LENGTH_LONG).show();}
                if(saved)Toast.makeText(this,"JSON yedeği kaydedildi.",Toast.LENGTH_SHORT).show();
            }
            return;
        }
        if(requestCode!=FILE_PICKER_REQUEST)return;
        if(uploadCallback!=null){
            Uri uri=resultCode==RESULT_OK&&data!=null?data.getData():null;
            uploadCallback.onReceiveValue(uri==null?null:new Uri[]{uri});
            uploadCallback=null;
        } else if(resultCode==RESULT_OK){
            Toast.makeText(this,"Dosya seçimi uygulama yeniden açıldığı için tamamlanamadı. Tekrar seçin.",Toast.LENGTH_LONG).show();
        }
    }
    @Override public void onBackPressed() {
        if(view != null && view.canGoBack()) view.goBack(); else super.onBackPressed();
    }
    @Override public void onDestroy() {
        pendingBackup=null;
        if(uploadCallback!=null){uploadCallback.onReceiveValue(null);uploadCallback=null;}
        if(view != null){view.stopLoading();view.removeJavascriptInterface("KaloriAndroid");view.destroy();view=null;}
        super.onDestroy();
    }
}
