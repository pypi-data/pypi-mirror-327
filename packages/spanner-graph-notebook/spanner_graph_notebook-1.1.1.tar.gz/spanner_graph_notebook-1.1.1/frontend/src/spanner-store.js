/**
 * Copyright 2024 Google LLC
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

if (typeof process !== 'undefined' && process.versions && process.versions.node) {
    GraphConfig = require('./spanner-config');
    Node = require('./models/node');
    Edge = require('./models/edge');
}

/**
 * @callback GraphConfigCallback
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback FocusedGraphObjectCallback
 * @param {GraphObject|null} focusedGraphObject - The graph object currently focused. If null, nothing is focused.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback SelectedGraphObjectCallback
 * @param {GraphObject|null} selectedGraphObject - The graph object currently selected. If null, nothing is selected.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback SelectedGraphColorSchemeCallback
 * @param {GraphConfig.ColorScheme} colorScheme - The color scheme to use for nodes.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback ViewModeChangedCallback
 * @param {GraphConfig.ViewModes} ViewMode - Whether to show the graph, table, or schema view.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback LayoutModeChangedCallback
 * @param {GraphConfig.LayoutModes} layoutMode - The layout of the nodes (i.e. force directed, DAG, etc...)
 * @param {LayoutModes} lastLayoutMode - The previous layout used.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

/**
 * @callback ShowLabelsCallback
 * @param {Boolean} visible - Whether the labels are visible or not.
 * @param {GraphConfig} config - The graph configuration.
 * @returns {void}
 */

class GraphStore {
    /**
     * The configuration that the graph store is based on.
     * @type {GraphConfig}
     */
    config;

    /**
     * @type {Object.<string, string>}
     * An object to store reserved colors keyed by label.
     */
    reservedColorsByLabel = {};

    /**
     * @type {Array.<string>}
     * An array to store reserved colors for neighborhoods.
     */
    reservedColorsByNeighborhood = [];


    static EventTypes = Object.freeze({
        CONFIG_CHANGE: Symbol('configChange'),
        FOCUS_OBJECT: Symbol('focusObject'),
        SELECT_OBJECT: Symbol('selectObject'),
        COLOR_SCHEME: Symbol('colorScheme'),
        VIEW_MODE_CHANGE: Symbol('viewModeChange'),
        LAYOUT_MODE_CHANGE: Symbol('layoutModeChange'),
        SHOW_LABELS: Symbol('showLabels')
    });

    /**
     * Events that are broadcasted to GraphVisualization implementations.
     * @type Map<GraphStore.EventTypes, GraphConfigCallback[]>.
     */
    eventListeners = {
        /**
         * Stores event listeners for config changes.
         * @type {GraphStore.EventTypes.CONFIG_CHANGE, GraphConfigCallback[]>}
         */
        [GraphStore.EventTypes.CONFIG_CHANGE]: [],
        /**
         * @type {GraphStore.EventTypes.FOCUS_OBJECT, FocusedGraphObjectCallback[]>}
         */
        [GraphStore.EventTypes.FOCUS_OBJECT]: [],
        /**
         * @type {GraphStore.EventTypes.SELECT_OBJECT, SelectedGraphObjectCallback[]>}
         */
        [GraphStore.EventTypes.SELECT_OBJECT]: [],
        /**
         * @type {GraphStore.EventTypes.COLOR_SCHEME, SelectedGraphColorSchemeCallback[]>}
         */
        [GraphStore.EventTypes.COLOR_SCHEME]: [],
        /**
         * @type {GraphStore.EventTypes.VIEW_MODE_CHANGE, ViewModeChangedCallback[]>}
         */
        [GraphStore.EventTypes.VIEW_MODE_CHANGE]: [],
        /**
         * @type {GraphStore.EventTypes.LAYOUT_MODE_CHANGE, LayoutModeChangedCallback[]>}
         */
        [GraphStore.EventTypes.LAYOUT_MODE_CHANGE]: [],
        /**
         * @type {GraphStore.EventTypes.SHOW_LABELS, ShowLabelsCallback[]>}
         */
        [GraphStore.EventTypes.SHOW_LABELS]: []
    };

    /**
     * The data store that a GraphVisualization implementation utilizes.
     * @param {GraphConfig|null} config
     */
    constructor(config) {
        if (!(config instanceof GraphConfig)) {
            config = new GraphConfig({
                nodesData: [],
                edgesData: [],
                colorScheme: GraphConfig.ColorScheme.LABEL,
                rowsData: [],
                schemaData: {}
            });
        }

        this.config = config;
    }

    /**
     * Adds an event listener for a specific event type.
     * @param {GraphStore.EventTypes} eventType - The event type to listen for.
     * @param {GraphConfigCallback} callback - The callback to execute when the event is triggered.
     */
    addEventListener(eventType, callback) {
        if (!this.eventListeners[eventType]) {
            throw Error('Invalid event type', eventType);
        }

        this.eventListeners[eventType].push(callback);
    }

    /**
     * @param {GraphConfig.ViewModes} viewMode
     */
    setViewMode(viewMode) {
        if (viewMode === this.config.viewMode) {
            return;
        }

        this.setFocusedObject(null);
        this.setSelectedObject(null);

        this.config.viewMode = viewMode;
        this.eventListeners[GraphStore.EventTypes.VIEW_MODE_CHANGE]
            .forEach(callback => callback(viewMode, this.config));
    }

    /**
     * @param {Boolean} visible
     */
    showLabels(visible) {
        this.config.showLabels = visible;
        this.eventListeners[GraphStore.EventTypes.SHOW_LABELS]
            .forEach(callback => callback(visible, this.config));
    }

    /**
     * @param {LayoutModes} layoutMode
     */
    setLayoutMode(layoutMode) {
        this.config.lastLayoutMode = this.config.layoutMode;
        this.config.layoutMode = layoutMode;
        this.eventListeners[GraphStore.EventTypes.LAYOUT_MODE_CHANGE]
            .forEach(callback => callback(layoutMode, this.config.lastLayoutMode, this.config));
    }

    /**
     * Sets the focused object in the graph and notifies all registered listeners about the focus change.
     * @param {Object} graphObject - The graph object to be focused.
     */
    setFocusedObject(graphObject) {
        this.config.focusedGraphObject = graphObject;
        this.eventListeners[GraphStore.EventTypes.FOCUS_OBJECT].forEach(callback => callback(graphObject, this.config));
    }

    /**
     * Sets the selected object in the graph and notifies all registered listeners about the selection change.
     * @param {Object} graphObject - The graph object to be selected.
     */
    setSelectedObject(graphObject) {
        this.config.selectedGraphObject = graphObject;
        this.eventListeners[GraphStore.EventTypes.SELECT_OBJECT].forEach(callback => callback(graphObject, this.config));
    }

    /**
     * Sets the new color scheme and notifies all registered listeners about the color scheme change.
     * @param {GraphConfig.ColorScheme} colorScheme - The new color scheme to use for nodes.
     */
    setColorScheme(colorScheme) {
        if (!colorScheme) {
            console.error('Color scheme must be provided', colorScheme);
        }

        this.config.colorScheme = colorScheme;
        this.eventListeners[GraphStore.EventTypes.COLOR_SCHEME].forEach(callback => callback(colorScheme, this.config));
    }

    getEdgesOfObject(graphObject) {
        if (!graphObject || !graphObject instanceof GraphObject) {
            return [];
        }

        if (graphObject instanceof Node) {
            return this.getEdgesOfNode(graphObject);
        }

        return [];
    }

    getEdgesOfNode(node) {
        if (!node || !node instanceof Node) {
            return [];
        }

        return this.getEdges().filter(edge => edge.source === node || edge.target === node);
    }

    getNodeById(id) {
        return this.getNodes().find(node => node.id === id);
    }

    getNeighborsOfObject(graphObject) {
        if (!graphObject || !graphObject instanceof GraphObject) {
            return [];
        }

        if (graphObject instanceof Node) {
            return this.getNeighborsOfNode(graphObject);
        }

        if (graphObject instanceof Edge) {
            return [graphObject.source, graphObject.target];
        }
    }

    getNeighborsOfNode(node) {
        if (!node || !node instanceof Node) {
            return [];
        }

        const edges = this.getEdgesOfNode(node);
        return edges.map(edge => edge.source === node ? edge.target : edge.source);
    }

    edgeIsConnectedToNode(edge, node) {
        if (!node || !node instanceof Node) {
            return false;
        }
        
        return edge.source === node || edge.target === node
    }

    nodeIsNeighborTo(node, potentialNeighbor) {
        return this.getNeighborsOfNode(node).includes(potentialNeighbor);
    }

    edgeIsConnectedToFocusedNode(edge) {
        return this.edgeIsConnectedToNode(edge, this.config.focusedGraphObject);
    }

    edgeIsConnectedToSelectedNode(edge) {
        return this.edgeIsConnectedToNode(edge, this.config.selectedGraphObject);
    }

    nodeIsNeighborToFocusedNode(node) {
        return this.nodeIsNeighborTo(node, this.config.focusedGraphObject);
    }

    nodeIsNeighborToSelectedNode(node) {
        return this.nodeIsNeighborTo(node, this.config.selectedGraphObject);
    }

    /**
     * Gets the color for a node based on its neighborhood.
     * @param {GraphObject} node - The node to get the color for.
     * @returns {string} The color for the node based on its neighborhood.
     */
    getColorForNodeByNeighborhood(node) {
        if (!node || typeof node.neighborhood !== 'number') {
            console.error('Node must have a neighborhood', node);
        }

        let index = this.reservedColorsByNeighborhood.indexOf(node.neighborhood);
        if (index === -1) {
            index = this.reservedColorsByNeighborhood.push(node.neighborhood) - 1;
        }

        if (index > this.config.colorPalette.length - 1) {
            console.error('Ran out of colors for neighborhood');
            return this.config.colorPalette[0];
        }

        return this.config.colorPalette[index];
    }

    /**
     * Gets the color for a node based on its label.
     * @param {GraphObject} node - The node to get the color for.
     * @returns {string} The color for the node based on its label.
     */
    getColorForNodeByLabel(node) {
        if (!node || !node.label) {
            console.error('Node must have a label', node);
        }

        switch (this.config.viewMode) {
            case GraphConfig.ViewModes.SCHEMA:
                const schemaColor = this.config.schemaNodeColors[node.label];
                if (schemaColor) {
                    return schemaColor;
                }
                break;
            case GraphConfig.ViewModes.DEFAULT:
                const nodeColor = this.config.nodeColors[node.label];
                if (nodeColor) {
                    return nodeColor;
                }
                break;
        }

        return 'rgb(100, 100, 100)';
    }

    /**
     * Gets the color for a node based on the specified color scheme.
     * @param {GraphObject} node - The node to get the color for.
     * @param {GraphConfig.ColorScheme} colorScheme - The color scheme to use.
     * @returns {string} The color for the node.
     * @throws {Error} If an invalid color scheme is provided.
     */
    getColorForNode(node) {
        switch (this.config.colorScheme) {
            case GraphConfig.ColorScheme.NEIGHBORHOOD:
                return this.getColorForNodeByNeighborhood(node);
            case GraphConfig.ColorScheme.LABEL:
                return this.getColorForNodeByLabel(node);
            default:
                throw Error('Invalid color scheme', colorScheme);
        }
    }

    /**
     * @returns {Array<Node>|*[]}
     */
    getNodes() {
        switch (this.config.viewMode) {
            case GraphConfig.ViewModes.DEFAULT:
                return this.config.nodes;
            case GraphConfig.ViewModes.SCHEMA:
                return this.config.schemaNodes;
            default:
                return [];
        }
    }

    /**
     * @returns {Array<Edge>|*[]}
     */
    getEdges() {
        switch (this.config.viewMode) {
            case GraphConfig.ViewModes.DEFAULT:
                return this.config.edges;
            case GraphConfig.ViewModes.SCHEMA:
                return this.config.schemaEdges;
            default:
                return [];
        }
    }

    getEdgeDesign(edge) {
        const hasSelectedObject = this.config.selectedGraphObject
        const edgeIsSelected = this.config.selectedGraphObject && edge === this.config.selectedGraphObject;
        if (hasSelectedObject && edgeIsSelected) {
            return this.config.edgeDesign.selected;
        }

        if (hasSelectedObject) {
            if (this.edgeIsConnectedToSelectedNode(edge)) {
                return this.config.edgeDesign.focused;
            } else {
                return this.config.edgeDesign.default;
            }
        }

        const edgeIsFocused = this.config.focusedGraphObject && edge === this.config.focusedGraphObject;
        if (!hasSelectedObject && edgeIsFocused) {
            return this.config.edgeDesign.focused;
        }
        
        const isNeighbor = this.edgeIsConnectedToFocusedNode(edge) ||
            this.edgeIsConnectedToSelectedNode(edge);
        if (isNeighbor) {
            return this.config.edgeDesign.focused;
        }

        return this.config.edgeDesign.default;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = GraphStore;
}