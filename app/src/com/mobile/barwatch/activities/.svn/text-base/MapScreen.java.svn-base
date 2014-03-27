package com.mobile.barwatch.activities;

import android.location.*;
import android.os.Bundle;
import android.provider.Settings;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import java.util.*;

import com.mobile.barwatch.R;
import com.mobile.barwatch.Refreshable;
import com.mobile.barwatch.models.*;
import com.mobile.barwatch.R.drawable;
import com.mobile.barwatch.R.id;
import com.mobile.barwatch.R.layout;
import com.mobile.barwatch.R.menu;
import com.mobile.barwatch.listeners.*;

public class MapScreen extends Activity implements LocationListener, Refreshable {
	LocationManager locManager;		
	Location userLocation;			
	GoogleMap map;
	
	CameraPosition cp;

	OnInfoWindowClick infoListener;
	ArrayList<Bar> bars = new ArrayList<Bar>();
	
    @Override
    public void onCreate(Bundle savedInstanceState) {    	   	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.map_screen);
                
        map = ((MapFragment)getFragmentManager().findFragmentById(R.id.mapview)).getMap();
        map.setMyLocationEnabled(true);
        infoListener = new OnInfoWindowClick(this, new HashMap<Marker,Bar>());
        map.setOnInfoWindowClickListener(infoListener);
        
        locManager = (LocationManager)this.getSystemService(Context.LOCATION_SERVICE);
        List<String> providers = locManager.getProviders(true);
        for (String provider : providers) {
        	if (provider.equals(LocationManager.GPS_PROVIDER)) {
        		locManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 60000, 10, this);
        		userLocation = locManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        	} else if (provider.equals(LocationManager.NETWORK_PROVIDER)) {
        		locManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 60000, 10, this);
        		userLocation = locManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
        	}
        }
                
        if (userLocation != null) {
        	animateToPoint(userLocation);        	
        } else {
//        	Intent myIntent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
//        	startActivity(myIntent);
        }
                
        addBarsToMap();   
    }
    
    private void addBarsToMap() {
        try {        	
        	bars = Bar.getBarsFromDb();         	
        	for (Bar bar : bars) {          		
            	LatLng point = new LatLng(bar.latitude(), bar.longitude());                  	
            	Marker overlayItem = map.addMarker(new MarkerOptions()
        															.position(point)
        															.title(bar.name()+" ("+bar.coupons().size()+" coupons)")
																	.snippet(bar.address())
																	.icon(BitmapDescriptorFactory.fromResource(R.drawable.map_marker)));
            	infoListener.addMapEntry(overlayItem, bar);
        	}
        } catch (Exception e) {
        	System.out.println("Houston, we have a problem");
        	e.printStackTrace();
        }
    } 
    
    private void getBestLocation() {
    	
    }
    
    private void animateToPoint(Location point) {   
        cp = new CameraPosition.Builder()
        .target(new LatLng(point.getLatitude(),point.getLongitude()))
        .zoom(14)
        .build();                  
        map.animateCamera(CameraUpdateFactory.newCameraPosition(cp));
    }
    
    /**ACTIVITY OVERRIDES**/
    public void onResume() {
    	super.onResume();
    }
    
    public void onStart() {
    	super.onStart();
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
	/**END OVERRIDES**/
     
	/**MENU STUFF**/
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_initialization_screen, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        if (item.getItemId() == R.id.menu_refresh) {            
            this.refresh();
            return true;
        } else if (item.getItemId() == R.id.menu_quit) {
	    	this.quit();
	    	return true;
        } else if (item.getItemId() == R.id.menu_bars_list) {
        	this.asList();
        	return true;            
        } else {
            return super.onOptionsItemSelected(item);
        }
    }
    /**END MENU STUFF**/
    
    /**MENU ACTIONS**/
    public void refresh() { 
    	map.clear();
    	addBarsToMap();
    }
    
    public void quit() {
        locManager.removeUpdates(this); // no impact on GPS tracking        
        finish(); //destroy Android app        
    }
    
    public void asList() {
    	Intent i = new Intent(this, BarsList.class);
    	i.putParcelableArrayListExtra(Constants.BAR_EXTRA, this.bars);    	
    	this.startActivity(i);
    }
    /**END MENU ACTIONS**/
    
    /**LOCATION LISTENER STUFF**/    
    public void onLocationChanged(Location location) {
    	userLocation = location;
        this.animateToPoint(userLocation);
    }
    
    public void onProviderDisabled(String provider) {
        // TODO Auto-generated method stub    	

    }
    
    public void onProviderEnabled(String provider) {
    	userLocation = locManager.getLastKnownLocation(provider);
    	this.animateToPoint(userLocation);
    }
    
    public void onStatusChanged(String provider, int status, Bundle extras) {
        // TODO Auto-generated method stub
    }
    /**END LOCATION LISTENER STUFF**/ 
}
