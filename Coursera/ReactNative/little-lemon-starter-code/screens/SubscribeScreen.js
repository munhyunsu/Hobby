import * as React from 'react';
import { View, Image, Text, TextInput, Pressable, Alert, StyleSheet } from 'react-native';
import { validateEmail } from '../utils';

const SubscribeScreen = () => {
  // Add subscribe screen code here
  const [email, setEmail] = React.useState('');
  const [isValid, setIsValid] = React.useState(false);

  return (
    <View style={styles.container}>
      <Image
        style={styles.logo}
        source={require('../assets/little-lemon-logo-grey.png')} />
      <Text style={styles.regularText}>
        Subscribe to our newsletter for our latest delicious recipes!
      </Text>
      <TextInput
        style={styles.textInput}
        value={email}
        onChangeText={setEmail}
        keyboardType={'email-address'}
        placeholder={'Type your email'}/>
      <Pressable
        style={[styles.button, validateEmail(email) ? {backgroundColor: '#3E524B'} : {backgroundColor: 'gray'}]}
        onPress={() => Alert.alert('Thanks for subscribing, stay tuned!')}
        disabled={!validateEmail(email)}>
        <Text style={styles.buttonText}>
          Subscribe
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
    height: 117,
    width: 100,
    resizeMode: 'contain',
    borderRadius: 4,
  },
  regularText: {
    fontSize: 24,
    textAlign: 'center',
    padding: 24,
  },
  textInput: {
    width: '80%',
    padding: 8,
    margin: 16,
    fontSize: 18,
    backgroundColor: '#EDEFEE',
    borderColor: '#3E524B',
    borderWidth: 2,
    borderRadius: 8,
  },
  button: {
    width: '80%',
    backgroundColor: '#3E524B',
    borderColor: '#3E524B',
    borderRadius: 12,
    margin: 40,
    padding: 4,
  },
  buttonText: {
    fontSize: 18,
    color: '#EDEFEE',
    textAlign: 'center',
    padding: 8,
    paddingHorizontal: 32,
  },
});

export default SubscribeScreen;
