import { View } from 'react-native';
import LittleLemonHeader from './components/LittleLemonHeader';
import LittleLemonFooter from './components/LittleLemonFooter';

export default function App() {
  return (
    <View style={{ flex: 1, backgroundColor: 'green' }}>
      <View style={{ paddingTop: 30, backgroundColor: 'yellow' }}>
        <LittleLemonHeader />
      </View>
      <View style={{ flex: 1, backgroundColor: 'brown'}}>
      </View>
      <View style={{ backgroundColor: 'blue' }}>
        <LittleLemonFooter />
      </View>
    </View>
  );
}
