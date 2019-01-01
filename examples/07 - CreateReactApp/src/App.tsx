import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host( 'ws://localhost:8080' )

// Expose the `sayHelloJS` function to Python as `say_hello_js`
function sayHelloJS( x: any ) {
  console.log( 'Hello from ' + x )
}
// WARN: must use window.eel to keep parse-able eel.expose{...}
window.eel.expose( sayHelloJS, 'say_hello_js' )

// Test calling sayHelloJS, then call the corresponding Python function
sayHelloJS( 'Javascript World!' )
eel.say_hello_py( 'Javascript World!' )


interface IAppState {
  message: string
}

export class App extends Component<{}, {}> {
  public state: IAppState = {
    message: `Click button to choose a random file from the user's sustem`
  }

  public pickFile = () => {
    eel.pick_file('~')(( message: string ) => this.setState( { message } ) )
  }

  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>{this.state.message}</p>
          <button className='App-button' onClick={this.pickFile}>Pick Random File From `~/*`</button>
        </header>
      </div>
    );
  }
}

export default App;
