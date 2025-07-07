import {
 IconBellRinging,
 IconLogout,
 IconSwitchHorizontal,
} from '@tabler/icons-react';
import { Code, Group } from '@mantine/core';
import classes from '../src/assets/layout.module.css';
import { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

const data = [
 { link: '/', label: 'Homepage', icon: IconBellRinging },
];

export function Layout() {
 const [active, setActive] = useState('Homepage');
 const navigate = useNavigate();
 const links = data.map((item) => (
 <a
   className={classes.link}
   data-active={item.label === active || undefined}
   href={item.link}
   key={item.label}
   onClick={(event) => {
     event.preventDefault();
     setActive(item.label);
     navigate(item.link);
   }}
 >
   <item.icon className={classes.linkIcon} stroke={1.5} />
   <span>{item.label}</span>
 </a>
));


 return (
   <div className={classes.container}>
     <nav className={classes.navbar}>
       <div className={classes.navbarMain}>
         <Group className={classes.header} justify="space-between">
           <Code fw={700} className={classes.version}>
             v3.1.2
           </Code>
         </Group>
         {links}
       </div>

       <div className={classes.footer}>
         <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
           <IconSwitchHorizontal className={classes.linkIcon} stroke={1.5} />
           <span>Change account</span>
         </a>

         <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
           <IconLogout className={classes.linkIcon} stroke={1.5} />
           <span>Logout</span>
         </a>
       </div>
     </nav>
     <main className={classes.mainContent}>
       <Outlet />
     </main>
   </div>
 );
}