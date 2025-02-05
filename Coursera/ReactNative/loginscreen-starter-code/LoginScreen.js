import React, { useState } from 'react';
import { ScrollView, Text, StyleSheet, TextInput } from 'react-native';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerText}>Welcome to Little Lemon</Text>
      <Text style={styles.regularText}>Login to continue </Text>
      <TextInput
        style={styles.textInput}
        value={username}
        onChangeText={setUsername}
        placeholder={'Username'}
        keyboardType={'email-address'}
      />
      <TextInput
        style={styles.textInput}
        value={password}
        onChangeText={setPassword}
        placeholder={'Password'}
        secureTextEntry={true}
      />
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
  textInput: {
    margin: 16,
    padding: 8,
    backgroundColor: '#EDEFEE',
  },
});


