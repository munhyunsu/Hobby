import * as React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function LittleLemonFooter() {
  return (
    <View style={styles.container}> 
      <Text style={styles.text}>
        All rights reserved by Little Lemon, 2022{' '}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F4CE14',
    marginBottom: 10,
  },
  text: {
    fontSize: 18,
    color: 'black',
    textAlign: 'center',
  },
});
