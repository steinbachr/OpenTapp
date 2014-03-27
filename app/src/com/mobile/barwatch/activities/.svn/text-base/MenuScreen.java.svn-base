package com.mobile.barwatch.activities;

import com.mobile.barwatch.R;
import com.mobile.barwatch.models.Menu;
import com.mobile.barwatch.models.MenuItem;

import android.app.ListFragment;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;

public class MenuScreen extends ListFragment {		
	Menu menu;
	
	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		System.out.println("in Menu Fragment");
        super.onCreate(savedInstanceState);
        BarDetails hostActivity = (BarDetails)this.getActivity();        
                        
        this.menu = hostActivity.getBar().menu();
        
        if(this.menu != null) {        
	        ListAdapter myListAdapter = new ArrayAdapter<MenuItem>(
	        	    getActivity(),
	        	    R.layout.menu_item,
	        	    this.menu.menuItems());
		    setListAdapter(myListAdapter);
        }
	}
	
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
    	System.out.println("creating menu view"); 
        return inflater.inflate(R.layout.menu_screen, container, false);
    }
    
	@Override
	public void onConfigurationChanged(Configuration newConfig) {
	  super.onConfigurationChanged(newConfig);	  
	}

}
