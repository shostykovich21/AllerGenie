import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

export default function About() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Welcome to AllerGenie!!</Text>
      <Text style={styles.text}>
        Our Allergy Tracker app is designed to help you easily record and monitor your allergy symptoms. 
        You can upload photos of reactions or affected areas and describe your symptoms in detail. 
        Our goal is to provide you with a simple and effective way to keep track of your allergies over time.
      </Text>
      <Text style={styles.text}>
        Your health is important to us. We aim to make managing your allergies less stressful by organizing 
        your information in one convenient place. Whether you're consulting a doctor or just keeping personal records, 
        this app is here to support you.
      </Text>
      <Text style={styles.text}>
        If you have any questions, feedback, or suggestions, feel free to reach out to our support team. 
        We're continuously improving to provide the best experience possible.
      </Text>
      <Text style={styles.text}>Thank you for using our app!</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
    flexGrow: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#38A568',
    marginBottom: 20,
    textAlign: 'center',
  },
  text: {
    fontSize: 16,
    color: '#333',
    marginBottom: 15,
    lineHeight: 22,
  },
});
