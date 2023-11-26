import styles from '@/app/styles/loading.module.css';

export const LoadingScreen = () => {
    return (
        <div className={styles.loading_screen}>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
            <div className={styles.dot}></div>
        </div>
    );
};