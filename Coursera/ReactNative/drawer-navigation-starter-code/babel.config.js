module.exports = function(api) {
  api.cache(true);
  return {
    presets: [
      'babel-preset-expo',
      'module:metro-react-native-babel-preset'
    ],
    plugins: [
      '@babel/plugin-transform-export-namespace-from',
      'react-native-reanimated/plugin'
    ]
  };
};


