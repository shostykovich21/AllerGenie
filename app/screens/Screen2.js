import React, { useEffect } from 'react';
import { StyleSheet, Image } from 'react-native';
import { useNavigation } from '@react-navigation/native';

function Screen2() {
  const navigation = useNavigation();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.replace('AllergyEntry'); // Replace with your target screen name
    }, 3000); // 3000 ms = 3 seconds

    return () => clearTimeout(timer); // Cleanup on unmount
  }, []);

  return (
    <Image
      style={styles.imagestyle}
      source={{
        uri: 'https://videos.openai.com/vg-assets/assets%2Ftask_01jvqc6wvsehzt7adxfv4tm55n%2F1747762572_img_0.webp?st=2025-05-23T05%3A26%3A25Z&se=2025-05-29T06%3A26%3A25Z&sks=b&skt=2025-05-23T05%3A26%3A25Z&ske=2025-05-29T06%3A26%3A25Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=8ebb0df1-a278-4e2e-9c20-f2d373479b3a&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=em6FEfifnyo7uTOUwL4ZDkCeR6ySbwjWxHaNzH1KuUE%3D&az=oaivgprodscus',
      }}
      resizeMode="cover"
    />
  );
}

const styles = StyleSheet.create({
  imagestyle: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
});

export default Screen2;