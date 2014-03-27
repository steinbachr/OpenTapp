package com.mobile.barwatch.listeners;

import java.util.HashMap;

import android.content.Context;
import android.content.Intent;

import com.google.android.gms.maps.GoogleMap.OnInfoWindowClickListener;
import com.google.android.gms.maps.model.Marker;
import com.mobile.barwatch.activities.BarDetails;
import com.mobile.barwatch.models.*;
import com.mobile.barwatch.*;

public class OnInfoWindowClick implements OnInfoWindowClickListener {
	Context context;
	HashMap<Marker,Bar> markerMap;
	
	public OnInfoWindowClick(Context c, HashMap<Marker,Bar> markerMap) {
		this.context = c;
		this.markerMap = markerMap;
	}
	
	public void addMapEntry(Marker m, Bar b) {
		this.markerMap.put(m, b);
	}
	
	public void onInfoWindowClick(Marker marker) {
		//get the bar associated with the clicked marker
		Bar clickedBar = this.markerMap.get(marker);
		Intent i = new Intent(this.context, BarDetails.class);		
		i.putExtra(Constants.BAR_EXTRA, clickedBar);
		this.context.startActivity(i);
	}
}
