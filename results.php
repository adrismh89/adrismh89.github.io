<html>
<body>
<?php
    foreach($_POST as $key=>$post_data){
        echo "You posted:" . $key . " = " . $post_data . "<br>";
    }
?>

</body>
</html>