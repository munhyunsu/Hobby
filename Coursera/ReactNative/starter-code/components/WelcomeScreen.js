import { View, Text } from 'react-native';


export default function WelcomeScreen() {
  return (
    <View
      style={{
        backgroundColor: 'pink',
    }}>
      <Text
        style={{
          textAlign: 'center',
      }}>
        Little Lemon is a charming neighborhood bistro that serves simple food and classic cocktails in a lively but casual environment. We would love to hear more about your experience with us!
      </Text>
    </View>
  );
}
