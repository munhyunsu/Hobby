/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, {Component} from 'react';
import {
    AppRegistry,
    StyleSheet,
    Text,
    View
} from 'react-native';
import GoogleFit, { Scopes, BucketUnit } from 'react-native-google-fit';


export default class App extends Component {
    componentDidMount() {
      GoogleFit.checkIsAuthorized().then(() => {
        console.log(GoogleFit.isAuthorized);
      });
      const options = {
        scopes: [
          Scopes.FITNESS_ACTIVITY_READ,
          Scopes.FITNESS_ACTIVITY_WRITE,
          Scopes.FITNESS_BODY_READ,
          Scopes.FITNESS_BODY_WRITE,
        ],
      }
      GoogleFit.authorize(options)
        .then((res) => {
          console.log('authorized >>>', res)
          GoogleFit.getDailyStepCountSamples({
            startDate: "2024-01-01T00:00:00.000Z",
            endDate: new Date().toISOString(),
            bucketUnit: BucketUnit.DAY,
            bucketInterval: 1,
          })
          .then((res) => {
            console.log('Received >>>', res);
          })
          .catch((err) => {
            console.log('Receving Error >>>', err);
          })
        })
        .catch((err) => {
          console.log('err >>> ', err)
        })
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.welcome}>
                    Welcome to React Native!
                </Text>
                <Text style={styles.instructions}>
                    To get started, edit index.js
                </Text>
                <Text style={styles.instructions}>
                    Double tap R on your keyboard to reload,{'\n'}
                    Shake or press menu button for dev menu
                </Text>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F5FCFF',
    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    instructions: {
        textAlign: 'center',
        color: '#333333',
        marginBottom: 5,
    },
});

export default App;
