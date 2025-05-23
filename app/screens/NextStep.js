import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import MenuModal from '../components/MenuModal'; // Adjust path if needed

export default function NextStep({ navigation }) {
  const [menuVisible, setMenuVisible] = useState(false);
  const [foodConsumed, setFoodConsumed] = useState('');
  const [age, setAge] = useState('');

  const handleMenuPress = () => {
    setMenuVisible(true);
  };

  const handleSubmit = () => {
    navigation.navigate('Results', { foodConsumed, age });
  };

  return (
    <View style={styles.container}>
      {/* Top Menu Icon */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleMenuPress}>
          <Ionicons name="menu" size={30} color="#000" />
        </TouchableOpacity>
      </View>

      <Text style={styles.label}>Food consumed recently:</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter food consumed recently"
        value={foodConsumed}
        onChangeText={setFoodConsumed}
      />

      <Text style={styles.label}>Age:</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter your age"
        keyboardType="numeric"
        value={age}
        onChangeText={setAge}
      />

      <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
        <Text style={styles.submitButtonText}>Submit</Text>
      </TouchableOpacity>

      {/* Menu Modal */}
      <MenuModal visible={menuVisible} onClose={() => setMenuVisible(false)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    position: 'absolute',
    top: 50,
    left: 20,
    zIndex: 10,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 100, // Adjusted to push textboxes lower
  },
  input: {
    borderWidth: 2,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginTop: 10,
  },
  submitButton: {
    marginTop: 50,
    backgroundColor: '#38A568',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});
