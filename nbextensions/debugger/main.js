/**
 * Jupyter debugger extension
 *
 * @module
 * @summary     Debugger
 * @description Interactive debugging in Jupyter notebook.
 * @version     0.1.0
 * @file        debugger/main.js
 * @author      Marek Cermak
 * @contact     macermak@redhat.com
 * @copyright   Copyright 2019 Marek Cermak <macermak@redhat.com>
 *
 * This source file is free software, available under the following license:
 *   MIT license
 *
 * This source file is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
 *
 * For details please refer to: https://github.com/CermakM/jupyter-tools
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

    const params = {
        init_delay: 500,
        update_delay: 1000,
    };


    /**
     * Update cell metadata with folding info,
     * so folding state can be restored after reloading notebook
     *
     * @param cm CodeCell or CodeMirror instance
     */
    function updateMetadata (cm) {
        // User can click on gutter of unselected cells,
        // so make sure we store metadata in the correct cell
        let cell = null;
        let selected_cell = Jupyter.notebook.get_selected_cell();

        // if cell is passed, speeds up computation significantly
        if ((cm instanceof codecell.CodeCell)) {
            cell = cm;
        }
        else if (selected_cell.code_mirror !== cm) {
            let cells = Jupyter.notebook.get_cells();

            for (let c of cells) {
                if (c.code_mirror === cm ) { cell = c; break; }
            }
        }
        else cell = selected_cell;

        // breakpoints
        cell.metadata.breakpoints  = $(cell.element)
            .find('.CodeMirror-line')
            .map( (idx, e) => {
                if ($(e).hasClass('has-breakpoint')) return {
                    'index': idx,
                    'element': e
                };
            });
    }

    /**
     * Activate breakpoints in CodeMirror options, don't overwrite other settings
     *
     * @param cell CodeCell instance
     */
    function activate_cm_breakpoints (cell) {
        let cm = cell.code_mirror;
        let gutters = cm.getOption('gutters').slice();

        if ( $.inArray("CodeMirror-breakpoints", gutters) < 0) {
            gutters.push('CodeMirror-breakpoints');

            cm.setOption('gutters', gutters);
            cm.on('gutterClick', (self, ln, gutter, event) => {
                let info = self.lineInfo(ln);

                if (info.gutterMarkers) {

                    // remove has-breakpoint class to the line wrapper
                    self.removeLineClass(ln, 'text', 'has-breakpoint');
                    // toggle gutter marker
                    self.setGutterMarker(ln, "CodeMirror-breakpoints", null);

                    // skip folds
                    if (info.gutterMarkers.hasOwnProperty('CodeMirror-foldgutter')) {
                        console.warn(
                            "Setting breakpoint on foldable line is not allowed."
                        );
                    }

                } else {
                    // breakpoint marker
                    let marker = document.createElement("div");
                    marker.innerHTML = "●";
                    marker.setAttribute('class', 'breakpoint');

                    // add has-breakpoint class to the line wrapper
                    self.addLineClass(ln, 'text', 'has-breakpoint');
                    // toggle gutter marker
                    self.setGutterMarker(ln, "CodeMirror-breakpoints", marker);
                }

                // update after delay, pass cell here
                setTimeout(() => updateMetadata(cell), params.update_delay);
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
            activate_cm_breakpoints(cell);

            cell.code_mirror.on('delete', updateMetadata);
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
                activate_cm_breakpoints(cell);

                cell.code_mirror.on('delete', updateMetadata);
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
        let link = document.createElement("link");

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
        let conf_sect;
        if (Jupyter.notebook) {
            // we're in notebook view
            conf_sect = Jupyter.notebook.config;
        } else {
            // we're some other view like dashboard, terminal, etc, so bail now
            return;
        }

        /* change default breakpoint gutter width */
        load_css( './main.css');

        if (Jupyter.notebook._fully_loaded) {
            setTimeout(function () {
                console.log('Breakpoints: Wait for', params.init_delay, 'ms');
                initExistingCells();
            }, params.init_delay);
        }
        else {
            events.one('notebook_loaded.Notebook', initExistingCells);
        }
    };

    return {load_ipython_extension : load_extension};

});
