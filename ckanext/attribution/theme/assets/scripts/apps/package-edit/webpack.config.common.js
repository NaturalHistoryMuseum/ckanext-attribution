'use strict';

const {VueLoaderPlugin} = require('vue-loader');

const webpackConfig = {
    entry:   [
        './src/app.js'
    ],
    resolve: {
        alias: {
            vue: 'vue/dist/vue.js'
        }
    },
    module:  {
        rules: [
            {
                test: /\.vue$/,
                use:  'vue-loader'
            },
            {
                test: /\.js$/,
                use:  'babel-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    output:  {
        library:       'package-edit',
        libraryTarget: 'umd',
        filename:      'package-edit.js',
        publicPath: '/assets/scripts/apps/package-edit/'
    },

};

module.exports = webpackConfig;