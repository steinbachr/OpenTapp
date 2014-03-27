package com.mobile.barwatch.activities;

import java.util.ArrayList;

import com.mobile.barwatch.R;
import com.mobile.barwatch.R.id;
import com.mobile.barwatch.R.layout;
import com.mobile.barwatch.R.menu;
import com.mobile.barwatch.models.Constants;
import com.mobile.barwatch.models.Bar;
import com.mobile.barwatch.models.Coupon;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;

public class BarsList extends Activity {
	ListView lv;
	ArrayList<Bar> bars;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.bars_list);		
        lv = (ListView)findViewById(R.id.bars_list);                       
        
        bars = this.getIntent().getParcelableArrayListExtra(Constants.BAR_EXTRA);        
                
        ActionBar actionBar = getActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
        
        lv.setAdapter(new ArrayAdapter<Bar>(this, R.layout.bars_list_item, this.bars));
		lv.setOnItemClickListener(new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) { 
				Bar bar = (Bar)parent.getItemAtPosition(position);				
			    Intent i = new Intent(getApplicationContext(), BarDetails.class);
			    
				Bundle b = new Bundle();	 
				b.putParcelable(Constants.BAR_EXTRA, bar);				
				
			    i.putExtras(b);			    
			    startActivity(i);
			}
		});	
	}
	
	public void refresh() {
		try {
			bars = Bar.getBarsFromDb();
		} catch(Exception e) {
			e.printStackTrace();
		}
		ArrayAdapter<Bar> newList = ((ArrayAdapter<Bar>)lv.getAdapter());
		newList.clear(); //didnt hit an error when fetching bars
		newList.addAll(bars);
		newList.notifyDataSetChanged();		
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
