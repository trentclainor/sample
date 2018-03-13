import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Truncate from 'react-truncate';


class ReadMore extends Component {
    constructor(...args) {
        super(...args);

        this.state = {
            readMore: true
        };

        this.toggleLines = this.toggleLines.bind(this);
    }

    toggleLines(event) {
        event.preventDefault();

        this.setState({
            readMore: !this.state.readMore
        });

        this.props.onShowMore && this.props.onShowMore(event);
    }

    render() {
        let {children, moreText, lessText, lines} = this.props;

        return (
            <Truncate
                ellipsis={(
                    <span>... <br/><a href='#' onClick={this.toggleLines}>{moreText}</a></span>
                )}
                lines={this.state.readMore && lines}
                options={this.props.options}>
                {children}
                {
                    this.state.readMore ?
                        null
                        :
                        <span><br/><a href='#' onClick={this.toggleLines}>{lessText}</a></span>
                }
            </Truncate>
        );
    }
}

ReadMore.defaultProps = {
    lines: 3,
    moreText: 'More',
    lessText: 'Less',
    options: {}
};

ReadMore.propTypes = {
    children: PropTypes.node.isRequired,
    moreText: PropTypes.node,
    lessText: PropTypes.node,
    options: PropTypes.object,
    onShowMore: PropTypes.func,
    lines: PropTypes.number
};

export default ReadMore;
