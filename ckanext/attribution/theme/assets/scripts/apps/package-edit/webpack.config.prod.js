'use strict';

const merge = require('webpack-merge');
const commonConfig = require('./webpack.config.common');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const {BundleStatsWebpackPlugin} = require('bundle-stats-webpack-plugin');

const webpackConfig = {
    mode        : 'production',
    resolve     : {
        alias: {
            vue: 'vue/dist/vue.esm.js'
        }
    },
    optimization: {
        minimizer: [
            new OptimizeCSSAssetsPlugin({
                cssProcessorPluginOptions: {
                    preset: ['default', {discardComments: {removeAll: true}}],
                }
            })
        ]
    },
    plugins     : [
        new BundleStatsWebpackPlugin({baseline: true})
    ],
    output      : {
        filename: '[name].package-edit.js'
    }
};

module.exports = merge(commonConfig, webpackConfig);