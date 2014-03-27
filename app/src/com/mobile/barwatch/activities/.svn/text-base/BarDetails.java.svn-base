package com.mobile.barwatch.activities;

import android.app.ActionBar;
import android.app.ActionBar.Tab;
import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import com.mobile.barwatch.R;
import com.mobile.barwatch.listeners.*;
import com.mobile.barwatch.models.Bar;
import com.mobile.barwatch.models.Constants;

public class BarDetails extends Activity {
	private static final String COUPON_LIST_TAG = "coupons";
	private static final String MENU_TAG = "menu";
	
	private Bundle barBundle;
	private Bar bar;	
	
	@Override
	public void onCreate(Bundle b) {
		System.out.println("In bar details");
		super.onCreate(b);
		
		ActionBar actionBar = getActionBar();
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
		actionBar.setDisplayHomeAsUpEnabled(true);
		
        barBundle = this.getIntent().getExtras();        
        bar = barBundle.getParcelable(Constants.BAR_EXTRA);                                    
        this.setTitle(bar.name());                  
		
        Tab tab = actionBar.newTab()
                .setText(R.string.coupons_tab)
                .setTabListener(new OnTabClick<CouponsList>(this, COUPON_LIST_TAG, CouponsList.class));
        actionBar.addTab(tab);
        tab = actionBar.newTab()
            .setText(R.string.menu_tab)
            .setTabListener(new OnTabClick<MenuScreen>(this, MENU_TAG, MenuScreen.class));
        actionBar.addTab(tab);               
	}	
	
	public Bundle getBarBundle() {
		return this.barBundle;
	}	
	public Bar getBar() {
		return this.bar;
	}
	
	public void refresh() {
	    CouponsList couponsFragment = (CouponsList)getFragmentManager().findFragmentByTag(COUPON_LIST_TAG);
		couponsFragment.refresh();
	}
	
	
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_screen_menus, menu);        
        return true;
    }   
    
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
	    if (item.getItemId() == android.R.id.home) {	        
            Intent intent = new Intent(this, MapScreen.class);
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
