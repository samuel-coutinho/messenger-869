import React from "react";
import { Box, Typography, Badge } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "space-between",
    marginLeft: 20,
    flexGrow: 1,
  },
  username: {
    fontWeight: "bold",
    letterSpacing: -0.2,
  },
  previewText: {
    fontSize: 12,
    color: "#9CADC8",
    letterSpacing: -0.17,
  },
  unreadmessages: {
  //  padding: 0,
  //  verticalAlign: "middle",
    right: "3vw",
//  top: "1vw",
    fontSize: 12,

  },
}));

const ChatContent = (props) => {
  const classes = useStyles();

  const { conversation } = props;
  const { latestMessageText, otherUser } = conversation;

  return (
    <Box className={classes.root}>
      <Box>
        <Typography className={classes.username}>
          {otherUser.username}
        </Typography>
        <Typography className={classes.previewText}>
          {latestMessageText}
        </Typography>
      </Box>
      { conversation.unreadMessages > 0 && 
        <Box alignItems="center">
          <Badge badgeContent={conversation.unreadMessages} max={99} color="primary" className={classes.unreadmessages} />
        </Box>
      }
    </Box>
  );
};

export default ChatContent;
