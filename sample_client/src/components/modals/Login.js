import {Button, ButtonToolbar, ControlLabel, FormControl, FormGroup, HelpBlock, Modal} from "react-bootstrap";
import React, { Component } from 'react';

function FieldGroup({ id, label, help, ...props }) {
  return (
    <FormGroup controlId={id}>
      <FormControl {...props} />
      {help && <HelpBlock>{help}</HelpBlock>}
    </FormGroup>
  );
}

class Login extends Component {
  render() {
    return (
        <div>
            <Modal bsSize={this.props.size} show={this.props.show} onHide={this.props.close} dialogClassName="login-modal">
              <Modal.Header closeButton>
                  <Modal.Title>Sign In</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                  <form>
                    <FieldGroup
                      id="formControlsEmail"
                      type="email"
                      placeholder="Enter email"
                    />
                    <FieldGroup
                      id="formControlsPassword"
                      placeholder="Enter password"
                      type="password"
                    />
                  </form>
              </Modal.Body>
              <Modal.Footer>
                <Button onClick={this.props.close}>Close</Button>
              </Modal.Footer>
            </Modal>
        </div>
    );
  }
};


export default Login;
