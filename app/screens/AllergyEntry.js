import React, { useState } from 'react';
import { View, Text, TextInput, Image, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';

import MenuModal from '../components/MenuModal';

export default function AllergyEntry({ navigation }) {
  const [imageUri, setImageUri] = useState(null);
  const [symptoms, setSymptoms] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [menuVisible, setMenuVisible] = useState(false);

  const pickImageFromGallery = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  const takePhotoWithCamera = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert("Permission Required", "Camera access is needed to take a photo.");
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleMenuPress = () => {
    setMenuVisible(true);
  };

  const handleNext = () => {
    navigation.navigate('NextStep', { imageUri, symptoms });
  };

  return (
    <View style={styles.container}>
      {/* Top Menu Icon */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleMenuPress}>
          <Ionicons name="menu" size={30} color="#000" />
        </TouchableOpacity>
      </View>

      <View style={styles.iconRow}>
        <TouchableOpacity onPress={pickImageFromGallery} style={styles.iconWrapper}>
          <Ionicons name="image-outline" size={40} color="#000" />
          <Text>Gallery</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={takePhotoWithCamera} style={styles.iconWrapper}>
          <Ionicons name="camera-outline" size={40} color="#000" />
          <Text>Camera</Text>
        </TouchableOpacity>
      </View>

      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}

      <TextInput
        style={[
          styles.input,
          { borderColor: isFocused ? '#50C878' : '#ccc' }
        ]}
        placeholder="Describe your symptoms..."
        multiline
        numberOfLines={4}
        value={symptoms}
        onChangeText={setSymptoms}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />

      {/* Bottom "Next" Button */}
      <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
        <Text style={styles.nextButtonText}>Next</Text>
      </TouchableOpacity>

      {/* Menu Modal */}
      <MenuModal visible={menuVisible} onClose={() => setMenuVisible(false)} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    paddingTop: 50,
    backgroundColor: '#fff',
  },
  header: {
    position: 'absolute',
    top: 50,
    left: 20,
    zIndex: 10,
  },
  iconRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 120,
    marginBottom: 20,
  },
  iconWrapper: {
    alignItems: 'center',
  },
  image: {
    width: 200,
    height: 200,
    alignSelf: 'center',
    marginBottom: 20,
    borderRadius: 10,
  },
  input: {
    borderWidth: 2,
    borderColor: '#ccc',
    padding: 10,
    marginTop: 30,
    marginBottom: 20,
    borderRadius: 5,
    textAlignVertical: 'top',
  },
  nextButton: {
    position: 'absolute',
    bottom: 70,
    left: 20,
    right: 20,
    backgroundColor: '#38A568',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  nextButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});
