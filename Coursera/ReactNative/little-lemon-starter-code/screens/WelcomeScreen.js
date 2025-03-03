import * as React from 'react';
import { View, Image, Text, Pressable, StyleSheet } from 'react-native';

const WelcomeScreen = ({ navigation }) => {
  // Add welcome screen code here.
  return (
    <View style={styles.container}>
      <Image
        style={styles.logo}
        source={require('../assets/little-lemon-logo.png')} />
      <Text style={styles.regularText}>
        Little Lemon, your local
        Mediterranean Bistro
      </Text>
      <Pressable
        style={styles.button}
        onPress={() => navigation.navigate('Subscribe')}>
        <Text style={styles.buttonText}>
          Newsletter
        </Text>
      </Pressable>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    height: 240,
    width: 136,
    resizeMode: 'contain',
    borderRadius: 4,
  },
  regularText: {
    fontSize: 32,
    textAlign: 'center',
    padding: 24,
  },
  button: {
    backgroundColor: '#3E524B',
    borderColor: '#3E524B',
    borderRadius: 12,
    margin: 40,
    padding: 6,
  },
  buttonText: {
    fontSize: 24,
    color: '#EDEFEE',
    textAlign: 'center',
    padding: 8,
    paddingHorizontal: 32,
  },
});

export default WelcomeScreen;
