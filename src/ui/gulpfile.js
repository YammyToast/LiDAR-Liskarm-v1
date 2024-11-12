const gulp = require("gulp");
const inline_source = require("gulp-inline-source");
const html_min = require("gulp-htmlmin");

gulp.task("inline", () => {
  return gulp
    .src("./src/index.html")
    .pipe(inline_source({ rootpath: "./src" }))
    .pipe(html_min({
        collapseWhitespace: true,
        removeComments: true,
        minifyCSS: true,
        minifyJS: true
    }))
    .pipe(gulp.dest('./dist'));
});

gulp.task('default', gulp.series('inline'));