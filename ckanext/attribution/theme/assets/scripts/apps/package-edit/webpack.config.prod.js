'use strict';

const merge = require('webpack-merge');
const commonConfig = require('./webpack.config.common');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSAssetsPlugin  = require('optimize-css-assets-webpack-plugin');

const webpackConfig = {
    mode: 'production',
    resolve: {
        alias: {
            vue: 'vue/dist/vue.esm.js'
        }
    },
    optimization: {
        minimizer: [
            new OptimizeCSSAssetsPlugin({
                cssProcessorPluginOptions: {
                    preset: [ 'default', { discardComments: { removeAll: true } } ],
                }
            }),
            new UglifyJSPlugin({
                cache: true,
                parallel: true,
                sourceMap: false
            })
        ]
    }
};

module.exports = merge(commonConfig, webpackConfig);