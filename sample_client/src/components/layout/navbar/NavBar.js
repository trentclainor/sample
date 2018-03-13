import React, {Component} from 'react';
import {
    Collapse, DropdownItem, DropdownMenu,
    DropdownToggle, Nav, Navbar, NavbarBrand,
    NavbarToggler, NavItem, NavLink,
    UncontrolledDropdown
} from 'reactstrap';
import logo from './logo.png'
import {authLogoutAndRedirect} from "../../../actions/auth";
import PropTypes from 'prop-types';
import {connect} from "react-redux";
import {BLOG_URL} from "../../../utils/config";
import {NavLink as NavigationLink} from "react-router-dom";

class NavBar extends Component {
    static propTypes = {
        isAuthenticated: PropTypes.bool.isRequired,
        dispatch: PropTypes.func.isRequired,
        location: PropTypes.shape({
            pathname: PropTypes.string
        })
    };

    logout = () => {
        this.props.dispatch(authLogoutAndRedirect());
    };

    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }
    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (
            <div>
                <Navbar className='bg-light' light expand="lg">
                    <NavbarBrand href="/">
                        <img src={logo} />
                    </NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar>
                        {this.props.isAuthenticated ?
                            <Nav className="ml-auto" navbar>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/" activeClassName="active" className='text-uppercase' exact>Home</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/search" activeClassName="active" className='text-uppercase'>Job Search</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink href={BLOG_URL} className='text-uppercase'>Articles</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/about" activeClassName='active' className='text-uppercase' exact>About</NavLink>
                                </NavItem>

                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/profile" activeClassName="active" className='text-uppercase' exact>Profile</NavLink>
                                </NavItem>
                                <UncontrolledDropdown nav className='px-md-3'>
                                    <DropdownToggle nav caret className='text-uppercase'>
                                        User
                                    </DropdownToggle>
                                    <DropdownMenu >
                                        <DropdownItem>
                                            Option 1
                                        </DropdownItem>
                                        <DropdownItem>
                                            Option 2
                                        </DropdownItem>
                                        <DropdownItem divider />
                                        <DropdownItem onClick={this.logout}>
                                            Logout
                                        </DropdownItem>
                                    </DropdownMenu>
                                </UncontrolledDropdown>
                            </Nav>
                            :
                            <Nav className="ml-auto" navbar>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/" activeClassName="active" exact>Home</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/about" activeClassName='active' exact>About</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink href={BLOG_URL}>Articles</NavLink>
                                </NavItem>
                                <NavItem className='px-md-3'>
                                    <NavLink tag={NavigationLink} to="/login" activeClassName="active" exact>Sign In</NavLink>
                                </NavItem>
                            </Nav>
                        }
                    </Collapse>
                </Navbar>
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        isAuthenticated: state.auth.isAuthenticated,
        location: state.routing.location
    };
};

export default connect(mapStateToProps)(NavBar);
export { NavBar as AppNotConnected };
