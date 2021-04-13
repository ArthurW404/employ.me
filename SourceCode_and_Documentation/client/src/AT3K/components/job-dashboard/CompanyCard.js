// import React from 'react';
// import { Link } from 'react-router-dom';
// import styles from './CardCarousel.module.scss';

// const CompanyCard = ({ name, description, link }) => {
//     return (
//         <div className={styles.companyCard}>
//             <h3 className={styles.title}>
//                 <Link to={`${link}?company=${name}`}>
//                     {name}
//                 </Link>
//                 {/* <a href={link}></a> */}
//             </h3>
//             <p className={styles.description}>
//                 {description}
//             </p>
//         </div>
//     )
// }

// export default CompanyCard;
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import { Link } from 'react-router-dom';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  root: {
    minWidth: 275,
    maxWidth: 300,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

const CompanyCard = ({ name, description, link }) => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography variant="h5" component="h2">
          {name}
        </Typography>
        <Typography variant="body2" component="p">
          {description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button 
            component={Link} 
            variant="outlined"
            to={`${link}?company=${name}`} 
            size="small"
        >
            View Profile
        </Button>
      </CardActions>
    </Card>
  );
}

export default CompanyCard;