import React, { Component } from 'react';

class Title extends Component {
    render() {
        return (
            <div className="Title">
                <div className="bg-brand-gradient mb-3">
                    <div className="container">
                        <div className="row align-items-center p-3">
                            { this.props.title ?
                                <h1 className="entry-title text-white">{this.props.title}</h1>
                                :
                                null
                            }

                            {this.props.children}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Title;
