module.exports = {
    env: {
        'jasmine': true,
        'commonjs': true
    },
    extends: [
        'plugin:json/recommended'
    ],
    /**
     * A set of overrides for JavaScript assets where we support ES2015+.
     * */
    overrides: [
        {
            files: [
                'media/js/**/*.es6.js',
            ],
            env: {
                'es2017': true
            }
        },
        {
            files: [
                'media/js/firefox/welcome/**/*.js',
                'media/js/firefox/whatsnew/**/*.js'
            ],
            env: {
                'es2017': true
            }
        },
        {
            files: [
                'webpack.config.js',
                'webpack.static.config.js',
                'tests/unit/karma.conf.js'
            ],
            env: {
                'node': true,
                'es2017': true
            },
            rules: {
                'strict': ['error', 'global'],
            }
        }
    ],
    globals: {
        'Mozilla': 'writable',
        'Mzp': 'writable',
        'site': 'writable'
    }
};
