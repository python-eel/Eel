declare global {
  interface Window {
    eel: {
      expose: (func: Function, name: string) => void;
      [key: string]: any;
    };
  }
}
export {};
