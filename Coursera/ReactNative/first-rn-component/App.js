import { View } from 'react-native';
import LittleLemonHeader from './components/LittleLemonHeader';

export default function App() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: '#495E57',
      }}>
      <LittleLemonHeader />
    </View>
  );
}
