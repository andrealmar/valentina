var $ = require('jquery-browserify');
var React = require('react');
var ReactDOM = require('react-dom');

// ReactJS components

var ChatHeading = React.createClass({
  render: function() {
    return (
      <div className="controls">
          <button>&times;</button>
          <h2>{this.props.chat.alias}</h2>
      </div>
    );
  }
});

var ChatTimeline =  React.createClass({
  render: function() {
    return (
      <div className="timeline">
        <ol>
          {this.props.messages.map(function(message){
            return (
              <li className={message.className} key={message.id} id={message.id}>
                <span className="author">{message.author}</span>
                <p>{message.content}</p>
                <span className="ago">{message.ago}</span>
              </li>
            );
          })}
        </ol>
      </div>
    );
  }
});

var ChatForm = React.createClass({
  getInitialState: function(){
    return {message: ''};
  },
  handleMessageChange: function(e){
    this.setState({message: e.target.value});
  },
  handleSubmit: function(e){
    e.preventDefault();
    var chat = this.props.chat.id;
    var content = this.state.message;
    if (!chat || !content) {
      return;
    }
    this.props.onMessageSubmit({content: content, chat: chat});
    this.setState({message: ''});
  },
  render: function(){
    return (
      <div className="input">
        <form onSubmit={this.handleSubmit}>
          <textarea onChange={this.handleMessageChange}></textarea>
          <button type="submit">Enviar</button>
        </form>
      </div>
    );
  }
});

var ChatBox = React.createClass({
  getInitialState: function(){
    return {chat: this.props.chat, messages: []};
  },
  scrollToLastMessage: function (){
    $("div.timeline").each(function(){
      $(this).animate({scrollTop: $(this).prop("scrollHeight")}, 500);
    });
  },
  loadMessages: function() {
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      cache: false,
      success: function(data){
        this.setState({chat: data['chat'], messages: data['messages']});
        this.scrollToLastMessage();
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleMessageSubmit: function(message){
    $.ajax({
      url: this.props.chat.url,
      dataType: 'json',
      type: 'POST',
      data: message,
      success: function(data) {
        this.setState({chat: data['chat'], messages: data['messages']});
        this.scrollToLastMessage();
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function(){
    this.loadMessages();
    setInterval(this.loadMessages, this.props.fetchInterval);
  },
  render: function() {
    return (
      <section className="col chat">
        <ChatHeading chat={this.state.chat} />
        <ChatTimeline messages={this.state.messages} />
        <ChatForm chat={this.state.chat} onMessageSubmit={this.handleMessageSubmit} />
      </section>
    );
  }
});

var ChatBoxes = React.createClass({
  getInitialState: function(){
    return {chats: this.props.chats};
  },
  render: function(){
    return(
      <div>
        {this.state.chats.map(function(chat){
          return (
            <ChatBox key={chat.key} chat={chat} fetchInterval={3000} />
          );
        })}
      </div>
    );
  }
});

// Get user chats and render ReactJS components

var get_chats = function () {
  var chats = [];
  $('li[data-chat-url]').each(function(){
    chats.push($(this).attr('data-chat-url'));
  });
  var re = /(\/app\/chat\/)(\d+)(\/)/;
  return chats.map(function(chat){
    return {
      key: chat.replace(/\//g, ''),
      id: re.exec(chat)[2],
      url: chat
    };
  });
};

ReactDOM.render(
  <ChatBoxes chats={get_chats()} />,
  document.getElementById('chat_panels')
);
