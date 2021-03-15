'use strict';

const {VueLoaderPlugin} = require('vue-loader');

module.exports = {
    mode:    'production',
    entry:   [
        './src/app.js'
    ],
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
    resolve: {
        alias: {
            vue: 'vue/dist/vue.js'
        }
    }
};