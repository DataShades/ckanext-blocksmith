const { src, dest, watch } = require("gulp");

const if_ = require("gulp-if");
const sourcemaps = require("gulp-sourcemaps");
const sass = require('gulp-sass')(require('sass'));
const touch = require("gulp-touch-fd");
const cleanCSS = require("gulp-clean-css");
const postcss = require("gulp-postcss");
const combineQueries = require("postcss-sort-media-queries");

const isDev = !!process.env.DEBUG;

const build = () =>
    src("ckanext/blocksmith/assets/scss/main.scss")
        .pipe(if_(isDev, sourcemaps.init()))
        .pipe(sass(
            {
                includePaths: ["node_modules"],
                // silenceDeprecations: ["import", "legacy-js-api"],
            }
        )).on("error", sass.logError)
        .pipe(postcss([combineQueries])) //  group identical @media queries into single block and sort them using mobile-first order
        .pipe(!isDev ? cleanCSS({
            compatibility: '*', // (default) - Internet Explorer 10+ compatibility mode
            level: 2 // Optimization levels. The level option can be either 0, 1 (default), or 2, e.g.
        }) : sourcemaps.write())
        .pipe(dest("ckanext/blocksmith/assets/css"))
        .pipe(touch());

const watchSource = () =>
    watch(
        "ckanext/blocksmith/assets/scss/**/*.scss",
        { ignoreInitial: false },
        build
    );
exports.watch = watchSource;
exports.build = build;
