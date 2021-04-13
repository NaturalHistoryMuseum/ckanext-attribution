'use strict';

const merge = require('webpack-merge');
const commonConfig = require('./webpack.config.common');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

const webpackConfig = {
    mode        : 'production',
    resolve     : {
        alias: {
            vue: 'vue/dist/vue.esm.js'
        }
    },
    optimization: {
        minimize   : true,
        minimizer  : [
            new OptimizeCSSAssetsPlugin({
                cssProcessorPluginOptions: {
                    preset: ['default', {discardComments: {removeAll: true}}],
                }
            }),
            new TerserPlugin({
                extractComments: false
            })
        ],
        splitChunks: {
            cacheGroups: {
                commons: {
                    test  : /[\\/]node_modules[\\/]/,
                    name  : 'vendors',
                    chunks: 'all',
                    maxSize: 200000
                }
            }
        }
    },
    plugins     : [
    ],
    output      : {
        filename: '[name].package-edit.js',
    }
};

module.exports = merge(commonConfig, webpackConfig);