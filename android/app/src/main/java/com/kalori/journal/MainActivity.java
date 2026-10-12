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

public class MainActivity extends Activity {
    private WebView view;
    private static final int FILE_PICKER_REQUEST=301;
    private ValueCallback<Uri[]> uploadCallback;
    private static final String ASSET_ORIGIN = "file:///android_asset/";
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        view = new WebView(this);
        view.getSettings().setJavaScriptEnabled(true);
        view.getSettings().setDomStorageEnabled(true);
        view.getSettings().setAllowFileAccess(true);
        view.getSettings().setAllowContentAccess(false);
        view.getSettings().setAllowFileAccessFromFileURLs(false);
        view.getSettings().setAllowUniversalAccessFromFileURLs(false);
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
                if ("https".equals(uri.getScheme())) {
                    startActivity(new Intent(Intent.ACTION_VIEW,uri));
                }
                return true;
            }
        });
        setContentView(view);
        view.loadUrl(ASSET_ORIGIN+"index.html");
    }
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data) {
        super.onActivityResult(requestCode,resultCode,data);
        if(requestCode!=FILE_PICKER_REQUEST)return;
        if(uploadCallback!=null){
            Uri uri=resultCode==RESULT_OK&&data!=null?data.getData():null;
            uploadCallback.onReceiveValue(uri==null?null:new Uri[]{uri});
            uploadCallback=null;
        }
    }
    @Override public void onBackPressed() {
        if(view != null && view.canGoBack()) view.goBack(); else super.onBackPressed();
    }
    @Override public void onDestroy() {
        if(uploadCallback!=null){uploadCallback.onReceiveValue(null);uploadCallback=null;}
        if(view != null){view.destroy();view=null;}
        super.onDestroy();
    }
}
