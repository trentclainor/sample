import React, {Component} from 'react';
import PropTypes from 'prop-types';
import BlockUi from 'react-block-ui';
import {Loader as ReactLoader} from 'react-loaders';
import 'react-block-ui/style.css';
import 'loaders.css/loaders.min.css';


class Loader extends Component {
    render() {
        let {children, loading, loaderType, loaderColor} = this.props;
        return (
            <BlockUi tag="div" blocking={loading} keepInView={true} loader={<ReactLoader active type={loaderType} color={loaderColor}/>}>
                {children}
            </BlockUi>
        );
    }
}

Loader.defaultProps = {
    loaderType: 'ball-spin-fade-loader',
    loaderColor: '#04be9e',
    loading: false
};

Loader.propTypes = {
    children: PropTypes.node.isRequired,
    loaderType: PropTypes.node,
    loaderColor: PropTypes.node,
    loading: PropTypes.bool
};

export default Loader;
