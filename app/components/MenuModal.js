import React from 'react';
import {
  Modal,
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  TouchableWithoutFeedback,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function MenuModal({ visible, onClose }) {
  const navigation = useNavigation();

  const handleNavigation = (screen) => {
    onClose();
    navigation.navigate(screen);
  };

  return (
    <Modal transparent visible={visible} animationType="slide">
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay}>
          <TouchableWithoutFeedback>
            <View style={styles.modal}>
              <TouchableOpacity onPress={() => handleNavigation('About')}>
                <Text style={styles.menuItem}>About</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={() => handleNavigation('History')}>
                <Text style={styles.menuItem}>History</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={() => handleNavigation('HealthcareServices')}>
                <Text style={styles.menuItem}>Healthcare Service</Text>
              </TouchableOpacity>
            </View>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  modal: {
    backgroundColor: 'white',
    paddingVertical: 20,
    paddingHorizontal: 30,
    marginTop: 60,
    marginLeft: 20,
    borderRadius: 10,
    elevation: 5,
  },
  menuItem: {
    fontSize: 18,
    marginVertical: 10,
    color: '#38A568', // updated color
    fontWeight: '600',
  },
});
