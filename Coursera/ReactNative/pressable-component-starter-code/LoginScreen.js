import React, { useState } from 'react';
import { View, ScrollView, Text, StyleSheet, TextInput, Pressable } from 'react-native';

export default function LoginScreen() {
  const [email, onChangeEmail] = useState('');
  const [password, onChangePassword] = useState('');
  const [loggedIn, onChangeLoggedIn] = useState(false);

  const toggleLoggedIn = () => onChangeLoggedIn(!loggedIn);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerText}>Welcome to Little Lemon</Text>
        <Text style={styles.regularText}>
          {loggedIn ? 'You are logged in' : 'Login to continue'}
        </Text>
        {!loggedIn && (
          <View>
          <TextInput
            style={styles.inputBox}
            value={email}
            onChangeText={onChangeEmail}
            placeholder={'email'}
            keyboardType={'email-address'}
          />
          <TextInput
            style={styles.inputBox}
            value={password}
            onChangeText={onChangePassword}
            placeholder={'password'}
            keyboardType={'default'}
            secureTextEntry={true}
          />
            <Pressable
              style={styles.button}
              onPress={toggleLoggedIn}>
              <Text style={styles.buttonText}>
                Login
              </Text>
            </Pressable>
          </View>
        )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  headerText: {
    padding: 40,
    fontSize: 30,
    color: '#EDEFEE',
    textAlign: 'center',
  },
  regularText: {
    fontSize: 24,
    padding: 20,
    marginVertical: 8,
    color: '#EDEFEE',
    textAlign: 'center',
  },
  inputBox: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
    fontSize: 16,
    borderColor: 'EDEFEE',
    backgroundColor: '#EDEFEE',
  },
  button: {
    backgroundColor: '#EE9972',
    borderColor: '#EE9972',
    borderRadius: 12,
    margin: 40,
    padding: 6,
  },
  buttonText: {
    fontSize: 32,
    textAlign: 'center',
  },
});
