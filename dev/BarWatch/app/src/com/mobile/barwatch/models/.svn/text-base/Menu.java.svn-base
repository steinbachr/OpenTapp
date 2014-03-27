package com.mobile.barwatch.models;

import java.util.ArrayList;

import android.os.Parcel;
import android.os.Parcelable;

public class Menu implements Parcelable {
	private int id;
	private ArrayList<MenuItem> menuItems = new ArrayList<MenuItem>();
	
	public Menu(int id, ArrayList<MenuItem> items) {
		this.id = id;
		this.menuItems = items;	
	}
	public Menu(Parcel p) {		
		this.id = p.readInt();		
		p.readTypedList(menuItems, MenuItem.CREATOR);
	}
	
	public ArrayList<MenuItem> menuItems() {
		return this.menuItems;
	}
	
	public String toString() {
		return "Menu "+id;
	}
	
	/**PARCELABLE STUFF**/
    public static final Parcelable.Creator<Menu> CREATOR = new Parcelable.Creator<Menu>() {
    	public Menu createFromParcel(Parcel in) {
    		return new Menu(in);
    	}
		public Menu[] newArray(int size) {
			return new Menu[size];
		}
    };

    public int describeContents() {
        return 0;
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeInt(this.id);
        out.writeTypedList(this.menuItems);     
    }
    /**END PARCELABLE**/
}
