import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import MenuModal from '../components/MenuModal';

export default function Results({ navigation }) {
  const [menuVisible, setMenuVisible] = useState(false);

  const handleMenuPress = () => {
    setMenuVisible(true);
  };

  const handleShowHealthcare = () => {
    setMenuVisible(false);
    navigation.navigate('HealthcareServices');
  };

  const handleEmergencyRemedy = () => {
    alert('Emergency remedy clicked');
  };

  return (
    <View style={styles.container}>
      {/* Menu Icon */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleMenuPress}>
          <Ionicons name="menu" size={30} color="#000" />
        </TouchableOpacity>
      </View>

      {/* Center Title */}
      <Text style={styles.title}>Results</Text>

      {/* Buttons */}
      <TouchableOpacity style={styles.healthcareButton} onPress={handleShowHealthcare}>
        <Text style={styles.buttonText}>Show Nearby Healthcare Services</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.emergencyButton} onPress={handleEmergencyRemedy}>
        <Text style={styles.buttonText}>Emergency Remedy</Text>
      </TouchableOpacity>

      {/* Menu Modal */}
      <MenuModal visible={menuVisible} onClose={() => setMenuVisible(false)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 60,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
  },
  header: {
    position: 'absolute',
    top: 50,
    left: 20,
    zIndex: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 40,
  },
  healthcareButton: {
    backgroundColor: '#38A568',
    padding: 15,
    borderRadius: 10,
    marginVertical: 10,
    alignItems: 'center',
  },
  emergencyButton: {
    backgroundColor: '#E55454', // softer red
    padding: 15,
    borderRadius: 10,
    marginVertical: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});
