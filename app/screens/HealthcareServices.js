import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ActivityIndicator, Text } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';

export default function HealthcareServices() {
  const [location, setLocation] = useState(null);
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        alert('Permission to access location was denied');
        return;
      }

      let loc = await Location.getCurrentPositionAsync({});
      setLocation(loc.coords);
      fetchPlaces(loc.coords.latitude, loc.coords.longitude);
    })();
  }, []);

  const fetchPlaces = async (lat, lon) => {
    const query = `
      [out:json];
      (
        node(around:3000,${lat},${lon})[amenity=hospital];
        node(around:3000,${lat},${lon})[amenity=clinic];
        node(around:3000,${lat},${lon})[amenity=pharmacy];
      );
      out body;
    `;
    const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;

    try {
      const response = await fetch(url);
      const data = await response.json();
      setPlaces(data.elements);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching healthcare services:', error);
      setLoading(false);
    }
  };

  if (loading || !location) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#38A568" />
        <Text style={{ marginTop: 10 }}>Loading nearby services...</Text>
      </View>
    );
  }

  return (
    <MapView
      style={styles.map}
      region={{
        latitude: location.latitude,
        longitude: location.longitude,
        latitudeDelta: 0.03,
        longitudeDelta: 0.03,
      }}
    >
      <Marker
        coordinate={{ latitude: location.latitude, longitude: location.longitude }}
        title="You are here"
        pinColor="blue"
      />
      {places.map((place, idx) => (
        <Marker
          key={idx}
          coordinate={{ latitude: place.lat, longitude: place.lon }}
          title={place.tags.name || 'Healthcare Service'}
          description={place.tags.amenity}
          pinColor="#38A568"
        />
      ))}
    </MapView>
  );
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
