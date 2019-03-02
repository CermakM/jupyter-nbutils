/**
 * Jupyter debugger extension
 *
 * @module
 * @author Marek Cermak <macermak@redhat.com>
 *
 * This module adds breakpoint functionality to CodeMirror gutters
 * and enables usege of enhanced cell debugging.
 */

define([
    'base/js/namespace',
    'jquery',
    'require',
    'base/js/events',
    'services/config',
    'notebook/js/codecell',
    'codemirror/lib/codemirror',
], function (Jupyter, $, requirejs, events, configmod, codecell, CodeMirror) {
    'use strict';

    var params = {
      init_delay: 500
    };

    /**
    * Activate breakpoints in CodeMirror options, don't overwrite other settings
    *
    * @param cm codemirror instance
    */
    function activate_cm_breakpoints (cm) {
      let gutters = cm.getOption('gutters').slice();

      if ( $.inArray("CodeMirror-breakpoints", gutters)) {
        gutters.push('CodeMirror-breakpoints');

        cm.setOption('gutters', gutters);
        cm.on('gutterClick', (self, ln) => {
          let info = self.lineInfo(ln);

          // breakpoint marker
          let marker = document.createElement("div");
          marker.innerHTML = "●";
          marker.setAttribute('class', 'breakpoint');
          marker.setAttribute('data-cm-cell-line', ln);

          self.setGutterMarker(
            ln, "CodeMirror-breakpoints", info.gutterMarkers ? null : marker);
          });
      }
    }

    /**
    * Add breakpoint gutter to a new cell
    *
    * @param event
    * @param nbcell
    *
    */
    var createCell = function (event, nbcell) {
      let cell = nbcell.cell;
      if ((cell instanceof codecell.CodeCell)) {
        activate_cm_breakpoints(cell.code_mirror);
      }
    };

    /*
    * Initialize gutter in existing cells
    *
    */
    var initExistingCells = function () {
      let cells = Jupyter.notebook.get_cells();
      cells.forEach( cell => {
        if ((cell instanceof codecell.CodeCell)) {
          activate_cm_breakpoints(cell.code_mirror);
        }
      });

      events.on('create.Cell', createCell);
    };

    /**
    * Load my own CSS file
    *
    * @param name off CSS file
    *
    */
    var load_css = function (name) {
      var link = document.createElement("link");
      link.type = "text/css";
      link.rel = "stylesheet";
      link.href = requirejs.toUrl(name, 'css');

      document.getElementsByTagName("head")[0].appendChild(link);
    };

    /**
     * Initialize extension
     *
     */
    var load_extension = function () {
        // first, check which view we're in, in order to decide whether to load
        var conf_sect;
        if (Jupyter.notebook) {
            // we're in notebook view
            conf_sect = Jupyter.notebook.config;
        }
        else if (Jupyter.editor) {
            // we're in file-editor view
            conf_sect = new configmod.ConfigSection('notebook', {base_url: Jupyter.editor.base_url});
            conf_sect.load();
        }
        else {
            // we're some other view like dashboard, terminal, etc, so bail now
            return;
        }

        /* change default breakpoint gutter width */
        load_css( './main.css');

        if (Jupyter.notebook) {
            if (Jupyter.notebook._fully_loaded) {
              setTimeout(function () {
                console.log('Breakpoints: Wait for', params.init_delay, 'ms');
                initExistingCells();
              }, params.init_delay);
            }
            else {
              events.one('notebook_loaded.Notebook', initExistingCells);
            }
        }
        else {
            activate_cm_breakpoints(Jupyter.editor.codemirror);
            setTimeout(function () {
                console.log('Breakpoints: Wait for', params.init_delay, 'ms');
                Jupyter.editor.codemirror.refresh();
            }, params.init_delay);
        }
    };

    return {load_ipython_extension : load_extension};

});
