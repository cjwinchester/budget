module.exports = function(grunt) {
  'use strict';

  grunt.initConfig({
    copy: {
      fonts: {
        src: [
          'node_modules/font-awesome/fonts/**'
        ],
        dest: 'static/budget/fonts/',
        flatten: true,
        expand: true
      }
    },
    less: {
      options: {
        sourceMap: true,
        paths: ['node_modules/bootstrap/less']
      },
      prod: {
        options: {
          compress: true,
          cleancss: true
        },
        files: {
          "static/budget/css/style.css": [
            "node_modules/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css",
            "src/less/style.less"
          ]
        }
      }
    },
    uglify: {
      options: {
        sourceMap: true
      },
      prod: {
        files: {
          'static/budget/js/scripts.js': [
            'node_modules/jquery/dist/jquery.js',
            'node_modules/underscore/underscore-min.js',
            'node_modules/bootstrap/js/tooltip.js',            'node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker.js',
            'node_modules/chart.js/dist/Chart.bundle.js',
            'node_modules/Chart.Annotation.js/Chart.Annotation.js',
            'src/js/main.js'
            ]
        }
      }
    },
    watch: {
      styles: {
        files: ['src/less/**/*.less'],
        tasks: ['less']
      },
      scripts: {
        files: ['src/js/**/*.js'],
        tasks: ['uglify']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');
  
  grunt.registerTask('default', ['copy:fonts','uglify', 'less', 'watch']);

};