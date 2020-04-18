window.addEventListener("load", () => {
  const editor = document.getElementById("editor-input");
  const preview = document.getElementById("preview");
  // axios cancel token
  let cancel = null;

  // Editor initialization
  const codemirror_editor = CodeMirror.fromTextArea(editor, {
    lineNumbers: true,
  });

  function printData(data) {
    preview.innerHTML = data;
  }

  /**
   * Делает запрос на бэк с передачей в query-string параметра q
   * В овете от серевера ожидает получить html
   * который в дальнейшем будет отрисован в правой панеле
   */
  async function fetchData(q) {
    if (cancel) {
      cancel();
    }
    const response = await axios.get(`/preview?q=${btoa(q)}`, {
      cancelToken: new axios.CancelToken((c) => {
        cancel = c;
      }),
    });
    const text = response.data;
    printData(text);
  }

  codemirror_editor.on("change", (instance) => {
    fetchData(instance.getValue());
  });
});
