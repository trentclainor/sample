import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Card, CardBody, CardHeader, Collapse} from "reactstrap";
import Icon from "./icon";

class CollapsibleCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isOpen: props.isOpen
        };

        this.toggle = this.toggle.bind(this);
    }

    toggle(event) {
        event.preventDefault();

        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        let {children, title, className} = this.props;

        return (
            <Card className={className}>
                <CardHeader >
                    <h5 className="mb-0">
                        <a href="javascript:void(0)" onClick={this.toggle}>
                            {title}
                            {
                                this.state.isOpen ?
                                    <span className="collapse-indicator float-right"><Icon name='caret-down'/></span>
                                    :
                                    <span className="collapse-indicator float-right"><Icon name='caret-right'/></span>
                            }

                        </a>
                    </h5>
                </CardHeader>
                <Collapse isOpen={this.state.isOpen}>
                    <CardBody className="pt-0 pb-0 mt-0 mb-0">
                        {children}
                    </CardBody>
                </Collapse>
            </Card>
        );
    }
}

CollapsibleCard.defaultProps = {
    isOpen: false,
    title: 'Card Title',
    options: {}
};

CollapsibleCard.propTypes = {
    children: PropTypes.node.isRequired,
    title: PropTypes.node,
    options: PropTypes.object,
    isOpen: PropTypes.bool
};

export default CollapsibleCard;
