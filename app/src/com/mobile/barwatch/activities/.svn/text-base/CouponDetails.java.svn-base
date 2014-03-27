package com.mobile.barwatch.activities;

import java.util.ArrayList;

import com.mobile.barwatch.R;
import com.mobile.barwatch.Refreshable;
import com.mobile.barwatch.R.id;
import com.mobile.barwatch.R.layout;
import com.mobile.barwatch.R.menu;
import com.mobile.barwatch.models.*;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.content.Context;
import android.content.Intent;

public class CouponDetails extends Activity implements Refreshable {
	Bundle barBundle;
	Bar bar;
	Coupon coupon;
	MobileUser mu;	
	
	public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.coupon_details);                
        
        mu = new MobileUser(this);              
        
        ActionBar actionBar = getActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true); 
        
        this.refresh();	//make sure we're up to date
        
        barBundle = this.getIntent().getExtras();        
        bar = barBundle.getBundle(Constants.BAR_EXTRA).getParcelable(Constants.BAR_EXTRA);	//this is kindve crappy, but we do this because passed in a bundle containing a bundle which contains the bar
        coupon = barBundle.getParcelable(Constants.COUPON_EXTRA);

        TextView couponDescTv = (TextView)findViewById(R.id.coupon_desc_text);
        TextView couponsRemainingTv = (TextView)findViewById(R.id.coupons_remaining_text);
        TextView timeRemainingTv = (TextView)findViewById(R.id.time_remaining_text);
        
        couponDescTv.setText(coupon.couponType());        
        couponsRemainingTv.setText(Integer.toString(coupon.numRemaining()));
        timeRemainingTv.setText(Integer.toString(coupon.timeRemaining() / 60));
	}
	
	public void onPause() {
		super.onPause();
	}
	
	public void onDestroy() {
		super.onDestroy();
	}
	
	public void onStop() {
		super.onStop();
	}
	
	public void redeemCoupon(View v) {
		if (!this.coupon.useCoupon()) { //the coupon can't be redeemed
			//TODO: might be worthwhile to display reason why cant redeem here
			this.finish();
		}									
		
		String redemptionResult = mu.redeemCoupon(this.coupon.id());
		
		/**CREATE THE DIALOG TO ENCAPSULATE THE SERVER RESPONSE **TAKEN FROM http://stackoverflow.com/questions/4283038/does-alertdialog-support-webview****/
		LayoutInflater inflater = LayoutInflater.from(this);			
		WebView couponWebView = new WebView(this);
		couponWebView.loadData(redemptionResult, "text/html", "UTF-8");
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setView(couponWebView);
		AlertDialog dialog = builder.show();
	}
	
	public void refresh() {
		try {			
			this.coupon = coupon.getCouponFromDb();			
	        TextView couponsRemainingTv = (TextView)findViewById(R.id.coupons_remaining_text);
	        TextView timeRemainingTv = (TextView)findViewById(R.id.time_remaining_text);	        
	        couponsRemainingTv.setText(Integer.toString(coupon.numRemaining()));        
	        timeRemainingTv.setText(Integer.toString(coupon.timeRemaining() / 60));		
		} catch(Exception e) {
			//refresh failed
		}			
	}
	
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_screen_menus, menu);
        this.refresh();	//make sure we arent working with stale data
        return true;
    }    
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		if (item.getItemId() == android.R.id.home) {
            Intent intent = new Intent(this, BarDetails.class);
            intent.putExtra(Constants.BAR_EXTRA, bar);
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP); 		           	      	  	
      	  	this.startActivity(intent);	      	  	
            return true;
		} else if (item.getItemId() == R.id.menu_refresh) {
        	this.refresh();
            return true;
		} else {
			return super.onOptionsItemSelected(item);
		}
	}
}
