import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  root: {
      "text-transform": "none",
      background: "linear-gradient(to right, #313335, #232526)",
      borderRadius: "15px",
      border: 0,
      color: 'white',
      height: 48,
      padding: '0 30px',
  },
};

function ClassNames(props) {
  const { classes, children, className, ...other } = props;

  return (
    <Button className={`${clsx(classes.root, className)}`} {...other}>
      {children || 'class names'}
    </Button>
  );
}

ClassNames.propTypes = {
  children: PropTypes.node,
  classes: PropTypes.object.isRequired,
  className: PropTypes.string,
};

export default withStyles(styles)(ClassNames);