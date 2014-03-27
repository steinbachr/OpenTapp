package com.mobile.barwatch.activities;

import java.util.*;

import android.app.ListFragment;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.content.Intent;
import android.content.res.Configuration;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.mobile.barwatch.R;
import com.mobile.barwatch.models.*;

public class CouponsList extends ListFragment {
	Bundle barBundle;
	Bar bar;
	List<Coupon> barCoupons = new ArrayList<Coupon>();
	ArrayAdapter<Coupon> myListAdapter;
	
	public void onActivityCreated(Bundle savedInstanceState) {
		System.out.println("in coupon list");
        super.onCreate(savedInstanceState);
        BarDetails hostActivity = (BarDetails)this.getActivity();        
        
        this.barBundle = hostActivity.getBarBundle();
        this.bar = hostActivity.getBar();
        this.barCoupons = this.bar.coupons();       
        this.myListAdapter = new ArrayAdapter<Coupon>(
        	    getActivity(),
        	    R.layout.coupon_list_item,
        	    this.barCoupons);        
	    setListAdapter(myListAdapter);    	         
	}
	
	@Override
	public void onConfigurationChanged(Configuration newConfig) {
	  super.onConfigurationChanged(newConfig);	  
	}
	
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
    	System.out.println("creating coupons list view"); 
        return inflater.inflate(R.layout.coupons_list, container, false);
    }
	
	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		Coupon coupon = (Coupon)l.getItemAtPosition(position);				
	    Intent i = new Intent(getActivity(), CouponDetails.class);
	    
		Bundle b = new Bundle();	 
		b.putParcelable(Constants.COUPON_EXTRA, coupon);
		b.putBundle(Constants.BAR_EXTRA, barBundle);
		
	    i.putExtras(b);			    
	    startActivity(i);
	}
	
    @Override
	public void onPause() {
		super.onPause();
	}
	
    @Override
	public void onDestroy() {
		super.onDestroy();
	}
	
	public void refresh() {
		ArrayList<Bar> bars = new ArrayList<Bar>();
		try {
			bars = Bar.getBarsFromDb();
			for (Bar b : bars) {
				if (b.id() == this.bar.id()) {
					this.barCoupons = b.coupons();						
				}
			}
		} catch (Exception e) {
			
		}
		
		if (bars.size() > 0) {	
			myListAdapter.clear();
			myListAdapter.addAll(this.barCoupons);
			myListAdapter.notifyDataSetChanged();
		}		
	}
}
